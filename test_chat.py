from qdrant_client import QdrantClient
from utils.contextual_chat_search import contextual_chat_search
from utils.terminal import clear_terminal, print_stream, print_markdown

# get user input from terminal
user_query = input("Enter your query: ")

# chat completion but streaming
# response = contextual_chat_search(user_query, stream=True)

# ollama
response = contextual_chat_search(user_query, stream=True, is_ollama=True)

# for chunk in response:
#     print(chunk.choices[0].delta.content, end="", flush=True)

clear_terminal()
markdown = print_stream(response)
clear_terminal()
print_markdown(markdown)
