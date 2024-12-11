from utils.chunk_pdf import chunk_pdf
from utils.qdrant_embed import qdrant_embed_docs

pdf_path = "data/article1.pdf"

docs = chunk_pdf(pdf_path)

# print chunks in loop
for i, chunk in enumerate(docs):
    # print chunkpdf_path 
    print(f"Chunk {i}: =================================================")
    print(chunk.page_content)

qdrant_embed_docs(docs)

print("done")