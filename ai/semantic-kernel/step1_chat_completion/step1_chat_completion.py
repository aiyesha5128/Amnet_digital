# Step 1: Azure OpenAI Chat Completion with Semantic Kernel (Credentials Masked)
# pyright: reportMissingImports=false
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion

# Initialize the Kernel object
kernel = Kernel()

# Masked credentials (replace with your actual values securely)
deployment_name = "MASKED_DEPLOYMENT_NAME"  # e.g., "gpt-4o-mini"
endpoint = "https://MASKED_RESOURCE_NAME.openai.azure.com/"
api_key = "MASKED_API_KEY"

# Remove previous services (safe to re-run)
kernel.remove_all_services()

# Add AzureChatCompletion service to the kernel
kernel.add_service(
    AzureChatCompletion(
        service_id="default",
        deployment_name=deployment_name,
        endpoint=endpoint,
        api_key=api_key,
    )
)
print("AzureChatCompletion added as service id 'default'")

import asyncio
from semantic_kernel.connectors.ai.prompt_execution_settings import PromptExecutionSettings
from semantic_kernel.agents.channels.chat_history_channel import ChatHistory
import nest_asyncio

chat = kernel.get_service("default")

async def test():
    settings = PromptExecutionSettings(
        deployment_name=deployment_name,
        model_id=deployment_name,  # Optional, if required
        temperature=0.7,
        max_tokens=256
    )
    chat_history = ChatHistory()
    chat_history.add_user_message("You are a helpful assistant. User: What is 2 + 2?")
    response = await chat.get_chat_message_content(chat_history, settings)
    print("Raw response object:", response)
    try:
        print("\n---- text ----\n", response.text)
    except Exception:
        pass

nest_asyncio.apply()
asyncio.run(test())
