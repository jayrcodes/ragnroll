from utils.qdrant_embed import qdrant_ollama_embed
from utils.helpers import print_doc_chunks

def main():
    from utils.chunk_webpage import chunk_webpage

    url = input("Enter the URL of the webpage to fetch: ")

    docs = chunk_webpage(url)

    print_doc_chunks(docs)

    qdrant_ollama_embed(docs, {
        "url": url
    })

    print("\nEmbedding complete.\n")

main()