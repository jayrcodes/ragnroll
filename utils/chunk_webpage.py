from langchain.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import re

def strip_multiple_newlines(text):
    # Replace two or more consecutive newlines with a single newline
    return re.sub(r'\n+', '\n', text)

def chunk_webpage(url: str):
    loader = WebBaseLoader(url)

    documents = loader.load()

    for document in documents:
        document.page_content = strip_multiple_newlines(document.page_content)
        document.page_content = document.page_content.strip()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.split_documents(documents)

    return docs

