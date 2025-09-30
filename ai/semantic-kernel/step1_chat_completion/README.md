# Step 1: Azure OpenAI Chat Completion with Semantic Kernel

This step demonstrates how to use the Semantic Kernel library to connect to Azure OpenAI and perform a simple chat completion. All credentials are masked for security.

## 📂 Folder Structure
```
semantic-kernel/
└── step1_chat_completion/
    ├── step1_chat_completion.py
    ├── README.md
    └── requirements.txt
```

## 🛠️ How to run
1. Install dependencies:
   ```bash
   pip install semantic-kernel[all]
   ```
2. Edit `step1_chat_completion.py` and set your Azure OpenAI credentials (deployment name, endpoint, API key).
3. Run the script:
   ```bash
   python step1_chat_completion.py
   ```

## 🔒 Security
- All credentials are masked in code.
- For production, use environment variables or a secure vault for credentials.

## 💡 Notes
- This is a minimal working example for beginners.
- See code comments for step-by-step explanations.
