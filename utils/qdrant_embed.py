from utils.chunk_webpage import chunk_webpage
from utils.generate_embeddings import get_embedding
from qdrant_client import QdrantClient, models
from utils.config import QDRANT_ENDPOINT
import uuid

def qdrant_embed_docs(docs):
    client = QdrantClient(url=QDRANT_ENDPOINT)

    document_id = str(uuid.uuid4())

    for idx, chunk in enumerate(docs):
        embedding = get_embedding(chunk.page_content)

        idx = idx + 1

        client.upsert(
            collection_name="acme",
            points=[
                models.PointStruct(
                    id=str(uuid.uuid4()),
                    vector=embedding.embedding,
                    payload={
                        "content": chunk.page_content,
                        "document_id": document_id,
                        "sequence": idx
                    }
                )
            ]
        )

    print("Success.")
