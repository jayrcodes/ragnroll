from openai import OpenAI
from utils.config import ENDPOINT, EMBEDDING_MODEL

client = OpenAI(base_url=ENDPOINT, api_key="lm-studio")

def get_embedding(text, model=EMBEDDING_MODEL):
    text = text.replace("\n", " ")
    return client.embeddings.create(input=[text], model=model).data[0]
