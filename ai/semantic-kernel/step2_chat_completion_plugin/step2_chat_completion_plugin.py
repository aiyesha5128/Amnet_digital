"""
step2_chat_completion_plugin.py

Translated from the notebook `semantic_kernel.ipynb` into a runnable script.
All credentials are read from environment variables — none are hard-coded here.

Before running (bash):
    export AZURE_OPENAI_ENDPOINT="https://<your-azure-openai-endpoint>/"
    export AZURE_OPENAI_API_KEY="<YOUR_AZURE_OPENAI_API_KEY>"
    export AZURE_OPENAI_DEPLOYMENT="gpt-4o-mini"

Run:
    python step2_chat_completion_plugin.py

"""

import os
import sys
import asyncio
from typing import Any

# Semantic Kernel imports
try:
    from semantic_kernel import Kernel
    from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion,AzureChatPromptExecutionSettings
        
    
    from semantic_kernel.functions import KernelArguments  # type: ignore[unused-import]
    from semantic_kernel.core_plugins.time_plugin import TimePlugin
    from semantic_kernel.connectors.ai import FunctionChoiceBehavior
    from semantic_kernel.contents import ChatHistory
    # Memory-related imports removed (not used in this demo)
except Exception as ex:
    print("ERROR: Failed to import Semantic Kernel components. Make sure 'semantic-kernel' is installed and the correct extras (azure) are present.")
    print("Import error:", ex)
    sys.exit(1)


def get_env(name: str) -> str:
    v = os.getenv(name)
    if not v:
        print(f"ERROR: environment variable {name} not set. Please set it before running.")
        sys.exit(1)
    return v


# Load required environment variables (masked)
AZURE_OPENAI_ENDPOINT = get_env("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY = get_env("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini")


# Kernel setup
kernel = Kernel()

# Add chat completion (Azure)
kernel.add_service(
    AzureChatCompletion(
        service_id="chat-gpt",
        deployment_name=AZURE_OPENAI_DEPLOYMENT,
        endpoint=AZURE_OPENAI_ENDPOINT,
        api_key=AZURE_OPENAI_API_KEY,
    )
)

# Add embedding service (Azure)
# Embedding service removed; this demo only exercises the TimePlugin and chat.

# Add Time plugin
kernel.add_plugin(TimePlugin(), plugin_name="TimePlugin")

# Chat execution settings (enable planning / function calling)
execution_settings = AzureChatPromptExecutionSettings()
execution_settings.function_choice_behavior = FunctionChoiceBehavior.Auto()
# Deterministic decoding for reproducible outputs during testing
execution_settings.temperature = 0.0
execution_settings.top_p = 0.0

# Create a chat history asking for the current time
history = ChatHistory()
history.add_message({"role": "user", "content": "What is the current time?"})

# Embedding service check removed: this demo does not use embeddings or Azure Cognitive Search.



async def main() -> None:
    # 1) Call the TimePlugin via the chat service
    try:
        plugin_result = await kernel.services["chat-gpt"].get_chat_message_content(
            chat_history=history,
            settings=execution_settings,
            kernel=kernel,
        )
        print("Plugin Output:", plugin_result)
    except Exception as ex:
        print("Plugin call failed:", ex)

    # 2) Invoke a prompt (TLDR example)
    prompt = (
        """
1) A robot may not injure a human being...
2) A robot must obey orders given it by human beings...
3) A robot must protect its own existence...

Give me the TLDR in exactly {{$num_words}} words. Only output {{$num_words}} words, nothing else.
"""
    )

    try:
        prompt_result = await kernel.invoke_prompt(prompt, arguments=KernelArguments(num_words=5))
        print("Prompt Output:", " ".join(str(prompt_result).split()[:5]))
    except Exception as ex:
        print("Prompt invocation failed:", ex)

    # No memory demo in this script. Remove Azure Cognitive Search / SemanticTextMemory usage.


if __name__ == "__main__":
    asyncio.run(main())
