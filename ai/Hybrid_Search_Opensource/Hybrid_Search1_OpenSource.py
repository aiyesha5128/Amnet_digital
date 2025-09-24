import os
#import os
os.environ["OPENAI_OPENAI_API_VERSION"] = "2025-01-01-preview"
import tempfile
import pickle
import numpy as np
from azure.storage.blob import BlobServiceClient
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from rank_bm25 import BM25Okapi
import faiss
from langchain_openai import AzureOpenAIEmbeddings, AzureChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain.docstore.document import Document


# Azure and OpenAI configuration (masked)
AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
CONTAINER_NAME = os.getenv("CONTAINER_NAME", "ai-search-dummy-data")
AZURE_FORM_RECOGNIZER_ENDPOINT = os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT")
AZURE_FORM_RECOGNIZER_KEY = os.getenv("AZURE_FORM_RECOGNIZER_KEY")

os.environ["AZURE_OPENAI_ENDPOINT"] = os.getenv("AZURE_OPENAI_ENDPOINT")
os.environ["AZURE_OPENAI_API_KEY"] = os.getenv("AZURE_OPENAI_API_KEY")
os.environ["AZURE_OPENAI_API_VERSION"] = os.getenv("AZURE_OPENAI_API_VERSION", "2025-01-01-preview")
os.environ["OPENAI_API_TYPE"] = os.getenv("OPENAI_API_TYPE", "azure")

# OCR cache directory
OCR_CACHE_DIR = "ocr_cache"
os.makedirs(OCR_CACHE_DIR, exist_ok=True)

def extract_text_with_ocr_cached(pdf_path, skip_empty=True):
    """
    Extract text from PDF using OCR with local caching.
    """
    cache_file = os.path.join(OCR_CACHE_DIR, os.path.basename(pdf_path) + ".pkl")
    if os.path.exists(cache_file):
        with open(cache_file, "rb") as f:
            print(f"♻️  Loading OCR from cache: {cache_file}")
            return pickle.load(f)
    form_client = DocumentAnalysisClient(
        endpoint=AZURE_FORM_RECOGNIZER_ENDPOINT,
        credential=AzureKeyCredential(AZURE_FORM_RECOGNIZER_KEY)
    )
    with open(pdf_path, "rb") as f:
        poller = form_client.begin_analyze_document("prebuilt-read", document=f)
    result = poller.result()
    extracted_text = []
    for page in result.pages:
        page_text = " ".join([line.content for line in page.lines])
        if skip_empty and len(page_text.strip()) == 0:
            continue
        extracted_text.append(page_text)
    with open(cache_file, "wb") as f:
        pickle.dump(extracted_text, f)
        print(f"💾 Saved OCR to cache: {cache_file}")
    return extracted_text

def main():
    # Connect to Azure Blob Storage
    blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
    container_client = blob_service_client.get_container_client(CONTAINER_NAME)

    # Download and process PDFs
    all_docs = []
    blobs = sorted(container_client.list_blobs(), key=lambda b: b.name)
    count = 0
    for blob in blobs:
        if blob.name.endswith(".pdf") and count < 1:
            count += 1
            print("Processing:", blob.name)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
                blob_client = container_client.get_blob_client(blob)
                data = blob_client.download_blob().readall()
                temp_pdf.write(data)
                temp_path = temp_pdf.name
            try:
                loader = PyPDFLoader(temp_path)
                pdf_docs = loader.load()
                ocr_lines = extract_text_with_ocr_cached(temp_path, skip_empty=True)
                num_pages = max(len(pdf_docs), len(ocr_lines))
                for i in range(num_pages):
                    structured_text = pdf_docs[i].page_content if i < len(pdf_docs) else ""
                    ocr_text = ocr_lines[i] if i < len(ocr_lines) else ""
                    if not structured_text.strip() and not ocr_text.strip():
                        continue
                    merged_text = structured_text + "\n" + ocr_text
                    doc = Document(
                        page_content=merged_text,
                        metadata={"source": blob.name, "page": i + 1}
                    )
                    all_docs.append(doc)
            finally:
                os.remove(temp_path)
                print(f"🗑️  Deleted temporary PDF: {temp_path}")
    print(f"✅ Loaded {len(all_docs)} non-empty pages with cached OCR")

    # BM25 and FAISS setup
    tokenized_corpus = [doc.page_content.split(" ") for doc in all_docs]
    bm25 = BM25Okapi(tokenized_corpus)

    embeddings_model = AzureOpenAIEmbeddings(
    azure_deployment="text-embedding-ada-002",   # deployment name in Azure
    model="text-embedding-ada-002",              # model type
    openai_api_key=os.environ["AZURE_OPENAI_API_KEY"],
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    openai_api_version=os.environ["AZURE_OPENAI_API_VERSION"]
)
    vector_embeddings = np.array(embeddings_model.embed_documents([doc.page_content for doc in all_docs])).astype("float32")
    embedding_dim = vector_embeddings.shape[1]
    faiss_index = faiss.IndexFlatL2(embedding_dim)
    faiss_index.add(vector_embeddings)
    faiss_id_to_doc = {i: doc for i, doc in enumerate(all_docs)}

    # Example hybrid search function
    def hybrid_search(query, top_k=3, alpha=0.5, candidate_factor=2):
        tokenized_query = query.lower().split()
        bm25_scores = bm25.get_scores(tokenized_query)
        bm25_norm = (bm25_scores - np.min(bm25_scores)) / (np.max(bm25_scores) - np.min(bm25_scores) + 1e-6)
        query_vector = np.array([embeddings_model.embed_query(query)]).astype("float32")
        distances, indices = faiss_index.search(query_vector, top_k * candidate_factor)
        faiss_top_indices = indices[0]
        bm25_top_indices = np.argsort(bm25_scores)[-top_k * candidate_factor:]
        candidate_indices = set(faiss_top_indices) | set(bm25_top_indices)
        hybrid_scores = []
        for i in candidate_indices:
            semantic_score = 0
            if i in faiss_top_indices:
                idx_pos = list(faiss_top_indices).index(i)
                semantic_score = 1 - distances[0][idx_pos]
            lexical_score = bm25_norm[i] if i in bm25_top_indices else 0
            final_score = alpha * semantic_score + (1 - alpha) * lexical_score
            hybrid_scores.append((all_docs[i], final_score))
        hybrid_results = sorted(hybrid_scores, key=lambda x: x[1], reverse=True)
        return [doc for doc, _ in hybrid_results[:top_k]]

    # Example LLM setup (Azure OpenAI)
    llm = AzureChatOpenAI(
        openai_api_key=os.environ["AZURE_OPENAI_API_KEY"],
        openai_api_version=os.environ["OPENAI_OPENAI_API_VERSION"],
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        deployment_name="gpt-4o-mini"
    )

    def rag_pipeline(query, top_k=3, alpha=0.6, candidate_factor=2):
        retrieved_docs = hybrid_search(query, top_k=top_k, alpha=alpha, candidate_factor=candidate_factor)
        context_texts = []
        for doc in retrieved_docs:
            citation = f"[{doc.metadata['source']}, Page {doc.metadata['page']}]"
            context_texts.append(f"{doc.page_content}\n{citation}")
        context = "\n\n".join(context_texts)
        prompt = f"Answer the question using the context below and provide sources for each point:\n\n{context}\n\nQuestion: {query}"
        response = llm.invoke(prompt)
        return response

    # Example usage
    query = "what is the information on internal use only."
    print(rag_pipeline(query))

if __name__ == "__main__":
    main()
