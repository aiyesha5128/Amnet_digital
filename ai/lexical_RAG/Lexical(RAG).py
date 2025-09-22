import os
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from azure.search.documents import SearchClient
from openai import AzureOpenAI
from azure.core.credentials import AzureKeyCredential

# Masked credentials and endpoints
AZURE_SEARCH_SERVICE = os.getenv("AZURE_SEARCH_SERVICE", "<YOUR_AZURE_SEARCH_SERVICE_ENDPOINT>")
AZURE_OPENAI_ACCOUNT = os.getenv("AZURE_OPENAI_ACCOUNT", "<YOUR_AZURE_OPENAI_ACCOUNT_ENDPOINT>")
AZURE_DEPLOYMENT_MODEL = os.getenv("AZURE_DEPLOYMENT_MODEL", "gpt-4o")
AZURE_SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY", "<YOUR_AZURE_SEARCH_KEY>")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY", "<YOUR_OPENAI_API_KEY>")

# Set up credentials and clients for standard Azure cloud
credential = DefaultAzureCredential()
token_provider = get_bearer_token_provider(credential, "https://cognitiveservices.azure.com/.default")

openai_client = AzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,  # Masked
    api_version="2024-06-01",
    azure_endpoint=AZURE_OPENAI_ACCOUNT,
    # azure_ad_token_provider=token_provider
)

search_client = SearchClient(
    endpoint=AZURE_SEARCH_SERVICE,
    index_name="multimodal-rag-1755860404874",
    # credential=credential,
    credential=AzureKeyCredential(AZURE_SEARCH_KEY)  # Masked
)

GROUNDED_PROMPT = """
You are a friendly assistant that answers technical queries about Price Increase processes, 
the Listener Messenger API, and Battery Low Delay Workflow.
Answer the query using only the sources provided below in a friendly and concise bulleted manner.
Answer ONLY with the facts listed in the list of sources below.
If there isn't enough information below, say you don't know.
Do not generate answers that don't use the sources below.
Query: {query}
Sources:
{sources}
"""

query = "What is the process for authenticating with the Listener Messenger API?"
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
    f"ID: {x['id']}, Document: {x['document_name']}, Chunk: {x['chunk_index']}, Type: {x['chunk_type']}, Words: {x['word_count']}, Chars: {x['character_count']}, Content: {x['content']}"
    for x in unique_chunks.values()
])

print("Sources used (unique):")
print(sources_formatted_unique)