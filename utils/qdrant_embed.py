from utils.chunk_webpage import chunk_webpage
from utils.generate_embeddings import get_embedding, ollama_embed
from qdrant_client import QdrantClient, models
from utils.config import QDRANT_ENDPOINT, QDRANT_COLLECTION
import pydash
import uuid

def qdrant_delete_by_metadata_key(key, value):
    client = QdrantClient(url=QDRANT_ENDPOINT)
    client.delete(
        collection_name=QDRANT_COLLECTION,
        points_selector=models.Filter(
            must=[
                models.FieldCondition(
                    key="metadata." + key,
                    match=models.MatchValue(value=value)
                )
            ]
        )
    )

# note in the future: an authenticated user should be included in the metadata duplicate deletion
def qdrant_embed_docs(docs, metadata = {}):
    client = QdrantClient(url=QDRANT_ENDPOINT)

    document_id = str(uuid.uuid4())
    
    document_title = pydash.get(metadata, "document_title")
    if document_title:
        qdrant_delete_by_metadata_key("document_title", document_title)

    url = pydash.get(metadata, "url")
    if url:
        qdrant_delete_by_metadata_key("url", url)

    for idx, chunk in enumerate(docs):
        embedding = get_embedding(chunk.page_content)

        idx = idx + 1

        payload={
            "content": chunk.page_content,
            "document_id": document_id,
            "sequence": idx,
            "metadata": metadata
        }

        client.upsert(
            collection_name=QDRANT_COLLECTION,
            points=[
                models.PointStruct(
                    id=str(uuid.uuid4()),
                    vector=embedding.embedding,
                    payload=payload
                )
            ]
        )

    print("\n\nSuccess.")

def qdrant_ollama_embed(docs, metadata = {}):
    client = QdrantClient(url=QDRANT_ENDPOINT)

    document_id = str(uuid.uuid4())
    
    document_title = pydash.get(metadata, "document_title")
    if document_title:
        qdrant_delete_by_metadata_key("document_title", document_title)

    url = pydash.get(metadata, "url")
    if url:
        qdrant_delete_by_metadata_key("url", url)

    for idx, chunk in enumerate(docs):
        # embedding = get_embedding(chunk.page_content)
        embedding = ollama_embed(chunk.page_content)

        idx = idx + 1

        payload={
            "content": chunk.page_content,
            "document_id": document_id,
            "sequence": idx,
            "metadata": metadata
        }

        client.upsert(
            collection_name="gte_qwen2",
            points=[
                models.PointStruct(
                    id=str(uuid.uuid4()),
                    vector=embedding,
                    payload=payload
                )
            ]
        )