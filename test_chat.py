from qdrant_client import QdrantClient
from utils.contextual_chat_search import contextual_chat_search

# get user input from terminal
user_query = input("Enter your query: ")

# chat completion but streaming
response = contextual_chat_search(user_query, stream=True)

print("\n\n")

for chunk in response:
    print(chunk.choices[0].delta.content, end="", flush=True)
