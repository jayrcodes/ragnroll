from utils.chunk_webpage import chunk_webpage
from utils.generate_embeddings import get_embedding
from qdrant_client import QdrantClient, models
from utils.config import QDRANT_ENDPOINT, QDRANT_COLLECTION
import uuid

def qdrant_delete_by_metadata_title(metadata_title):
    client = QdrantClient(url=QDRANT_ENDPOINT)
    client.delete(
        collection_name=QDRANT_COLLECTION,
        points_selector=models.Filter(
            must=[
                models.FieldCondition(
                    key="metadata_title",
                    match=models.MatchValue(value=metadata_title)
                )
            ]
        )
    )

# note in the future: an authenticated user should be included in the metadata duplicate deletion
def qdrant_embed_docs(docs, metadata_title):
    client = QdrantClient(url=QDRANT_ENDPOINT)

    document_id = str(uuid.uuid4())
    
    # delete existing data
    qdrant_delete_by_metadata_title(metadata_title)

    for idx, chunk in enumerate(docs):
        embedding = get_embedding(chunk.page_content)

        idx = idx + 1

        client.upsert(
            collection_name=QDRANT_COLLECTION,
            points=[
                models.PointStruct(
                    id=str(uuid.uuid4()),
                    vector=embedding.embedding,
                    payload={
                        "metadata_title": metadata_title,
                        "content": chunk.page_content,
                        "document_id": document_id,
                        "sequence": idx
                    }
                )
            ]
        )

    print("\n\nSuccess.")
