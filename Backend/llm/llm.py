import os
import dotenv
from langchain_groq import ChatGroq

def get_api_key():
    dotenv.load_dotenv()
    return os.getenv("GROQ_API_KEY") or os.getenv("LLM_KEY")

def create_llm():
    GROQ_API_KEY = get_api_key()
    if not GROQ_API_KEY:
        raise ValueError("API key not found. Check your .env file.")
    model_name = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
    return ChatGroq(
        model=model_name,
        temperature=0.7,
        api_key=GROQ_API_KEY,
    )

# llm = create_llm()

# messages = [
#     {"role": "system", "content": "You are a helpful assistant."},
#     {"role": "user", "content": "Hello, how are you?"}
# ]
# user_message = input("Enter your message: ")
# while user_message.lower() != "exit":
#     messages.append({"role": "user", "content": user_message})
#     response = llm.invoke(messages)
#     messages.append({"role": "assistant", "content": response.content})
#     print("Assistant:", response.content)
#     print("Conversation so far:")
#     for msg in messages:
#         print(f"{msg['role'].capitalize()}: {msg['content']}")

#     user_message = input("Enter your message (or type 'exit' to quit): ")

