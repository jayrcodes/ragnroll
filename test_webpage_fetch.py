from utils.chunk_webpage import chunk_webpage

# from user input
url = input("Enter the URL of the webpage to fetch: ")

docs = chunk_webpage(url)

# print chunks in loop
for i, chunk in enumerate(docs):
    # print chunk number
    print(f"Chunk {i}: =================================================")
    print(chunk.page_content)
