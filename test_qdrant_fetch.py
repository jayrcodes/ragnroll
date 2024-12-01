from qdrant_client import QdrantClient

# Initialize the client
client = QdrantClient(url="http://localhost:6333")  # Replace with your Qdrant instance URL

# Collection name
collection_name = "acme"

# Query by ID
point_id = 'a2ec1bb1-0017-4cd1-97b7-9870669623b5'  # Replace with the ID you used during insertion

response = client.retrieve(
    collection_name=collection_name,
    ids=[point_id],
    with_vectors=True
)

# Check if the vector exists
if response:
    print(f"Point ID {point_id} is stored: {response}")
else:
    print(f"Point ID {point_id} not found in the collection.")