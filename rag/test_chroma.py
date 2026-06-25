import chromadb

client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    name="test_collection"
)

print("ChromaDB Connected")
print(collection.name)