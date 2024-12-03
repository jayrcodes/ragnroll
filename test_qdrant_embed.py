from qdrant_client import QdrantClient, models
from utils.generate_embeddings import get_embedding
from utils.chunk_document import chunk_document
import uuid

client = QdrantClient(url="http://localhost:6333")

docs = chunk_document('data/article2.txt')

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
