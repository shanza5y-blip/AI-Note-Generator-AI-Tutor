import chromadb
from sentence_transformers import SentenceTransformer
import json

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection("notes_chunks")

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

query = "What is a process?"

embedding = model.encode(query).tolist()

results = collection.query(
    query_embeddings=[embedding],
    n_results=3,
    include=["documents", "metadatas"]
)

print("\n===== RETRIEVED DOCUMENTS =====\n")

for doc, meta in zip(
    results["documents"][0],
    results["metadatas"][0]
):
    print("TEXT:", doc)
    print(json.dumps(meta, indent=2))
    print("------------------------")