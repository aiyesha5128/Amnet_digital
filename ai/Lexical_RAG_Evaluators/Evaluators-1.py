import os



# Masked credentials: Set these as environment variables for security
AZURE_SEARCH_SERVICE = os.environ.get("AZURE_SEARCH_SERVICE")  # e.g., "https://<your-search-service>.search.windows.net"
AZURE_OPENAI_ACCOUNT = os.environ.get("AZURE_OPENAI_ACCOUNT")  # e.g., "https://<your-openai-account>.openai.azure.com/"
AZURE_DEPLOYMENT_MODEL = os.environ.get("AZURE_DEPLOYMENT_MODEL", "gpt-4o")
AZURE_OPENAI_API_KEY = os.environ.get("AZURE_OPENAI_API_KEY")
AZURE_SEARCH_KEY = os.environ.get("AZURE_SEARCH_KEY")

if not all([AZURE_SEARCH_SERVICE, AZURE_OPENAI_ACCOUNT, AZURE_OPENAI_API_KEY, AZURE_SEARCH_KEY]):
    raise ValueError("Please set all required Azure credentials as environment variables.")

# Install required packages (uncomment if running standalone)
# import sys
# !{sys.executable} -m pip install azure-search-documents openai azure-core azure-identity

from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from azure.search.documents import SearchClient
from openai import AzureOpenAI
from azure.core.credentials import AzureKeyCredential

# Set up credentials and clients for standard Azure cloud
credential = DefaultAzureCredential()
token_provider = get_bearer_token_provider(credential, "https://cognitiveservices.azure.com/.default")

openai_client = AzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    api_version="2024-06-01",
    azure_endpoint=AZURE_OPENAI_ACCOUNT,
    # azure_ad_token_provider=token_provider
)

search_client = SearchClient(
    endpoint=AZURE_SEARCH_SERVICE,
    index_name="multimodal-rag-1755860404874",
    # credential=credential
    credential=AzureKeyCredential(AZURE_SEARCH_KEY)
)

GROUNDED_PROMPT = """
You are a friendly assistant that answers technical queries about masked business processes.
Answer the query using only the sources provided below in a friendly and concise bulleted manner.
Answer ONLY with the facts listed in the list of sources below.
If there isn't enough information below, say you don't know.
Do not generate answers that don't use the sources below.
Query: {query}
Sources:
{sources}
"""

query = "MASKED_QUERY"
search_results = search_client.search(
    search_text=query,  # plain keyword match
    top=5  # get top 5 results
)
# Collect unique chunk IDs and filter sources to only unique chunks (up to top=5)
unique_chunks = {}
for x in search_results:
    if all(k in x for k in ['id','document_name','chunk_index','chunk_type','word_count','character_count','content']):
        if x['id'] not in unique_chunks and len(unique_chunks) < 5:
            unique_chunks[x['id']] = x

unique_chunk_ids = list(unique_chunks.keys())
print("Unique chunk IDs:", unique_chunk_ids)
print("Number of unique chunk IDs:", len(unique_chunk_ids))

# Print only unique, up-to-5 results from unique_chunks.values()
for x in unique_chunks.values():
    print(
        f"ID: {x['id']}, Document: {x['document_name']}, Chunk: {x['chunk_index']}, "
        f"Type: {x['chunk_type']}, Words: {x['word_count']}, Chars: {x['character_count']}, Content: {x['content']}"
    )

# Print only unique, up-to-5 results
sources_formatted_unique = "\n".join([
    f"ID: {x['id']}, Document: MASKED_DOCUMENT, Chunk: {x['chunk_index']}, Type: {x['chunk_type']}, Words: {x['word_count']}, Chars: {x['character_count']}, Content: {x['content']}"
    for x in unique_chunks.values()
])

for x in unique_chunks.values():
    print("Chunk Content:", x['content'])

print("Sources used (unique):")
print(sources_formatted_unique)

from azure.ai.evaluation import DocumentRetrievalEvaluator

# These query_relevance_labels are given by your human- or LLM-judges.
retrieval_ground_truth = [
    {"document_id": "1", "query_relevance_label": 4},
    {"document_id": "2", "query_relevance_label": 2},
    {"document_id": "3", "query_relevance_label": 3},
    {"document_id": "4", "query_relevance_label": 1},
    {"document_id": "5", "query_relevance_label": 0},
]
# The min and max of the label scores are inputs to document retrieval evaluator
ground_truth_label_min = 0
ground_truth_label_max = 4

# These relevance scores come from your search retrieval system
retrieved_documents = [
    {"document_id": "2", "relevance_score": 45.1},
    {"document_id": "6", "relevance_score": 35.8},
    {"document_id": "3", "relevance_score": 29.2},
    {"document_id": "5", "relevance_score": 25.4},
    {"document_id": "7", "relevance_score": 18.8},
]

document_retrieval_evaluator = DocumentRetrievalEvaluator(
    ground_truth_label_min=ground_truth_label_min, 
    ground_truth_label_max=ground_truth_label_max,
    ndcg_threshold=0.3,
    xdcg_threshold=30.0,
    fidelity_threshold=0.3,
    top1_relevance_threshold=2,
    top3_max_relevance_threshold=3,
    total_retrieved_documents_threshold=5,
    total_ground_truth_documents_threshold=5
)

results = document_retrieval_evaluator(
    retrieval_ground_truth=retrieval_ground_truth, 
    retrieved_documents=retrieved_documents
)
print("Document Retrieval Evaluation Results:", results)

from azure.ai.evaluation import GroundednessEvaluator

# Build context from the top 5 retrieved chunks
context = "\n".join([
    f"ID: {x['id']}, Document: MASKED_DOCUMENT, Chunk: {x['chunk_index']}, Type: {x['chunk_type']}, Words: {x['word_count']}, Chars: {x['character_count']}, Content: {x['content']}"
    for x in unique_chunks.values()
])

# Build the prompt using your GROUNDED_PROMPT and sources
prompt = GROUNDED_PROMPT.format(query=query, sources=context)

# Call the LLM (Azure OpenAI) to get the answer
completion = openai_client.chat.completions.create(
    model=AZURE_DEPLOYMENT_MODEL,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ],
    max_tokens=512,
    temperature=0.2
)

# Extract the response text
response = completion.choices[0].message.content

print("LLM Response:", response)
# Example response (replace with your actual model response)
#response = "[Your model's answer to the query goes here]"

# Model config (replace with your actual config if needed)
#model_config = {}  # or provide your model config dict
model_config = {
    "azure_endpoint": AZURE_OPENAI_ACCOUNT,
    "azure_deployment": AZURE_DEPLOYMENT_MODEL,
    "api_key": AZURE_OPENAI_API_KEY,
    "api_version": "2024-06-01"
}

# Run groundedness evaluation
groundedness = GroundednessEvaluator(model_config=model_config, threshold=4)
results = groundedness(
    query=query,
    context=context,
    response=response
)
print("Groundedness Evaluation Results:", results)

from azure.ai.evaluation import ResponseCompletenessEvaluator

response_completeness = ResponseCompletenessEvaluator(model_config=model_config, threshold=2)

result = response_completeness(
    response=response,
    ground_truth="MASKED_GROUND_TRUTH"
)

print("Response Completeness Evaluation Results:", result)
