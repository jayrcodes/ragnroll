from qdrant_client import QdrantClient
from utils.generate_embeddings import get_embedding
import json

# Initialize Qdrant client
# Update URL if using remote Qdrant
qdrant_client = QdrantClient(url="http://localhost:6333")

# query = " NASA deployed the device on a Gulfstream III aircraft flying over"
# query = "australia"
query = "Tell me more related to social media ban news"

embedded_query = get_embedding(query)

result = qdrant_client.search(
    collection_name="acme",
    query_vector=embedded_query.embedding,
    limit=3,
    search_params={"hnsw_ef": 256},
)

for doc in result:
    # to json
    print(doc.score)
    print(json.dumps(doc.payload, indent=4))
