import chromadb

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection("notes_chunks")

data = collection.get()

print("Total documents:", len(data["documents"]))

for i, doc in enumerate(data["documents"][:10]):
    print("\nDocument", i + 1)
    print(doc[:300])