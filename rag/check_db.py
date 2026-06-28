import chromadb

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection("notes_chunks")

data = collection.get()

print("Number of documents:", len(data["ids"]))