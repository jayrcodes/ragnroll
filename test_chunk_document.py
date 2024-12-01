from utils.chunk_document import chunk_document
from utils.helpers import pretty_print_docs
from utils.generate_embeddings import get_embedding

docs = chunk_document('data/article1.txt')

pretty_print_docs(docs)
