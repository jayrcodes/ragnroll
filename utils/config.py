import os
from dotenv import load_dotenv

load_dotenv()

ENDPOINT = os.getenv("ENDPOINT")
MODEL = os.getenv("MODEL")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION")
QDRANT_ENDPOINT = os.getenv("QDRANT_ENDPOINT")
API_PORT = int(os.getenv("API_PORT"))
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")
