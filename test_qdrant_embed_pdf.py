from utils.chunk_pdf import chunk_pdf, pdf_metadata
from utils.qdrant_embed import qdrant_embed_docs 
from utils.helpers import print_doc_chunks

pdf_path = "data/article1.pdf"

docs = chunk_pdf(pdf_path)

title = pdf_metadata(pdf_path)["title"]

print_doc_chunks(docs)

qdrant_embed_docs(docs, title)
