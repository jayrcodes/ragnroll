from qdrant_client import QdrantClient
from utils.generate_embeddings import get_embedding
from utils.chat_completions import chat_completion
from utils.config import QDRANT_COLLECTION, QDRANT_ENDPOINT

def contextual_chat_search(user_query, stream=False):
    qdrant_client = QdrantClient(url=QDRANT_ENDPOINT)

    embedded_query = get_embedding(user_query)

    result = qdrant_client.search(
        collection_name=QDRANT_COLLECTION,
        query_vector=embedded_query.embedding,
        limit=3,
        search_params={"hnsw_ef": 256},
    )

    # all content above score of 0.6, and merge content
    context = [doc.payload['content'] for doc in result if doc.score > 0.6]
    # print(context)

    prompt = f"""
    Context:
    {context}

    Task:
    {user_query}
    """

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt},
    ]

    # chat completion but streaming
    response = chat_completion(messages, stream)

    return response