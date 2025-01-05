
def pretty_print_docs(docs):
    for doc in docs:
        print(doc.page_content)
        print('-' * 100)

def print_doc_chunks(docs):
    for i, chunk in enumerate(docs):
        print(f"\nChunk {i}: =================================================\n")
        print(chunk.page_content)