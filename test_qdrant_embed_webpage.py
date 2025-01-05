from utils.chunk_webpage import chunk_webpage
from utils.qdrant_embed import qdrant_embed_docs
from utils.helpers import print_doc_chunks

# from user input
url = input("Enter the URL of the webpage to fetch: ")

docs = chunk_webpage(url)

# print_doc_chunks(docs)

qdrant_embed_docs(docs, {
    "url": url.strip()
})
