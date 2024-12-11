from utils.chunk_pdf import chunk_pdf

pdf_path = "data/article1.pdf"

result = chunk_pdf(pdf_path)

for i, doc in enumerate(result):
    # print chunk number
    print(f"Chunk {i+1}: =================================")
    print(doc.page_content)
