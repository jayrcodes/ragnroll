from openai import OpenAI
from utils.config import ENDPOINT, EMBEDDING_MODEL
from langchain_ollama import OllamaEmbeddings
from utils.config import OLLAMA_EMBEDDING_MODEL

client = OpenAI(base_url=ENDPOINT, api_key="lm-studio")

def get_embedding(text, model=EMBEDDING_MODEL):
    text = text.replace("\n", " ")
    return client.embeddings.create(input=[text], model=model).data[0]

def ollama_embed(text):
    embeddings = OllamaEmbeddings(model=OLLAMA_EMBEDDING_MODEL)
    return embeddings.embed_query(text)
