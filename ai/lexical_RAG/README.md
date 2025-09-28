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
   git clone https://github.com/your-username/aiyesha5128/lexical_RAG.git
   cd rag-experiments-demo
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

4. Run any of the Python demo files, e.g.:
   ```bash
   python Lexical(RAG).py
   ```

## 📂 Folder Structure
```
lexical_RAG/
│── Lexical_RAG.py
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
When you run a demo file, you might see output like:

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
```
