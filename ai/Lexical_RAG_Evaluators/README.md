# RAG Experiments Demo

This repository contains practice exercises using **Azure OpenAI** and **Azure AI Search** to build and test different Retrieval-Augmented Generation (RAG) pipelines.

## 📌 What this project does
- Demonstrates RAG pipelines using Azure services.
- Shows how to retrieve document chunks using lexical (keyword) search.
- This type is often called "RAG-Search" or "RAG with keyword/document search," and is commonly used for enterprise Q&A, technical support, or knowledge base assistants.
- Uses a language model to answer queries based only on retrieved sources.
- Prints and formats retrieved sources for inspection.
- All credentials are masked and should be set via environment variables.

## 🛠️ How to run
1. Clone the repository
   ```bash
   git clone https://github.com/aiyesha5128/Lexical_RAG_Evaluators.git
   cd Lexical_RAG_Evaluators
   ```
2. Install dependencies
   ```bash
   pip install azure-search-documents azure-identity openai azure-core
   ```
3. Set your Azure credentials as environment variables:
   - `AZURE_SEARCH_SERVICE`
   - `AZURE_OPENAI_ACCOUNT`
   - `AZURE_DEPLOYMENT_MODEL`
   - `AZURE_SEARCH_KEY`
   - `AZURE_OPENAI_API_KEY`

4. Run the Python demo file:
   ```bash
   python Evaluators-1.py
   ```

## 📂 Folder Structure
```
Lexical_RAG_Evaluators/
│── Evaluators-1.py
│── README.md
│── requirements.txt
```

## 🔒 Security
- All secrets and API keys are masked in code.
- Use environment variables or a secure vault for credentials.

## 💡 Notes
- This repo is for experimentation and learning.
- You can add more Python files to try different RAG approaches.
- See the code comments for details on each step.

## 🖨️ Example Output
When you run the demo file, you might see output like:

```
Unique chunk IDs: ['<CHUNK_ID_1>', '<CHUNK_ID_2>', ...]
Number of unique chunk IDs: 5
ID: <CHUNK_ID_1>, Document: <DOCUMENT_NAME>, Chunk: 3, Type: text_chunk, Words: 164, Chars: 985, Content: <MASKED_CONTENT>
...
Sources used (unique):
ID: <CHUNK_ID_1>, Document: <DOCUMENT_NAME>, Chunk: 3, Type: text_chunk, Words: 164, Chars: 985, Content: <MASKED_CONTENT>
...
LLM Response:
To authenticate with the Listener Messenger API, you must obtain an API key and include it in the Authorization header of your requests.

Document Retrieval Evaluation Results: {"ndcg": 0.85, "xdcg": 28.5, "fidelity": 0.92, "top1_relevance": 4, "top3_max_relevance": 3, "total_retrieved_documents": 5, "total_ground_truth_documents": 5}

Groundedness Evaluation Results: {"groundedness_score": 4.0, "is_grounded": true}

Response Completeness Evaluation Results: {"completeness_score": 2.0, "is_complete": true}
```
