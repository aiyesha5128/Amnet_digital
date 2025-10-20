# Step 2 — Chat Completion + Time Plugin (Semantic Kernel)

Lightweight demo that registers an Azure OpenAI chat/completion service in Semantic Kernel and calls the built‑in TimePlugin. This example intentionally omits embeddings / Azure Cognitive Search — credentials are read from environment variables only.

## 📂 Folder Structure
```
semantic-kernel/
└── step2_chat_completion_plugin/
    ├── step2_chat_completion_plugin.py
    ├── README.md
    └── requirements.txt
```



## Environment variables (required)
Set these in the same terminal session used to run the script.

Git Bash / WSL:
```bash
export AZURE_OPENAI_ENDPOINT="https://<your-azure-openai-endpoint>/"
export AZURE_OPENAI_API_KEY="<YOUR_AZURE_OPENAI_API_KEY>"
# optional
export AZURE_OPENAI_DEPLOYMENT="gpt-4o-mini"
```

PowerShell:
```powershell
$env:AZURE_OPENAI_ENDPOINT = "https://<your-azure-openai-endpoint>/"
$env:AZURE_OPENAI_API_KEY = "<YOUR_AZURE_OPENAI_API_KEY>"
# optional
$env:AZURE_OPENAI_DEPLOYMENT = "gpt-4o-mini"
```

CMD:
```cmd
set AZURE_OPENAI_ENDPOINT=https://<your-azure-openai-endpoint>/
set AZURE_OPENAI_API_KEY=<YOUR_AZURE_OPENAI_API_KEY>
```

Notes:
- Variables must be set in the same shell where you run `python`.
- To persist on Windows, use `setx` (then open a new shell).

Tip: a `.env.example` file is included in this folder. Copy it to `.env` and fill in values for local use:

```bash
cp .env.example .env
# then edit .env to add your keys
```

## 🔒 Security
- Do NOT hard-code secrets in code. Use environment variables, OS-level secret stores, or a secret manager (Azure Key Vault).
- Avoid committing `.env` files or files containing credentials to source control. Add them to `.gitignore`.
- For CI/CD, use pipeline secret variables or key vault integrations.

## How to run
From the folder containing `step2_chat_completion_plugin.py`:

```bash
python step2_chat_completion_plugin.py
```

## Expected output
- Plugin Output: <time-string>  (current time returned via TimePlugin)
- Prompt Output: <five-word-summary> (first 5 words from the TLDR prompt result)

Example:
```
Plugin Output: 2025-10-19 14:23:05
Prompt Output: Robots must never harm humans
```

```

## Installation
Install the Python dependency required by the script:

```bash
python -m pip install "semantic-kernel[azure]"
```

Or install from the included requirements file:

```bash
pip install -r requirements.txt
```

## Deterministic output
This script sets deterministic decoding (temperature=0, top_p=0) in its execution settings to make prompt outputs reproducible during testing. If you want more varied outputs, edit the script and change or remove these settings.


