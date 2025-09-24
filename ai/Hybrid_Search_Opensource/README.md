# Hybrid Search RAG Pipeline

This repository demonstrates a hybrid Retrieval-Augmented Generation (RAG) pipeline using **Azure OpenAI**, **Azure AI Search**, and semantic vector search (FAISS) with LangChain. It combines keyword (lexical) search and semantic search for improved document retrieval and question answering.

## 📌 What this project does
- Implements a hybrid RAG pipeline using Azure and LangChain.
- Retrieves document chunks using both BM25 keyword search and FAISS semantic search.
- Uses a language model to answer queries based on retrieved sources.
- Prints and formats retrieved sources for inspection.
- All credentials are masked and should be set via environment variables.

## 🛠️ How to run
1. Clone the repository
   ```bash
   git clone https://github.com/aiyesha5128/hybrid-search-opensource.git
   cd hybrid-search-opensource
   ```
2. Install dependencies
   ```bash
   pip install langchain openai azure-search-documents azure-identity azure-core faiss-cpu
   ```
3. Set your Azure and OpenAI credentials as environment variables:
   - `AZURE_SEARCH_SERVICE`
   - `AZURE_OPENAI_ACCOUNT`
   - `AZURE_DEPLOYMENT_MODEL`
   - `AZURE_SEARCH_KEY`
   - `AZURE_OPENAI_API_KEY`
   - Any other required keys for your pipeline

4. Run the main Python demo file:
   ```bash
   python Hybrid_Search1_OpenSource.py
   ```

## 📂 Folder Structure
```
Hybrid_search_OpenSource/
│── Hybrid_Search1_OpenSource.py
│── README.md
│── requirements.txt
│── .gitignore
```

## 🔒 Security
- All secrets and API keys are masked in code.
- Use environment variables or a secure vault for credentials.

## 💡 Notes
- This repo is for experimentation and learning.
- You can add more Python files to try different hybrid RAG approaches.
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
```
## 📄 License

This project is licensed under the MIT License. See the LICENSE file for details.
