import chromadb
from sentence_transformers import SentenceTransformer

client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_collection(
    "notes_chunks"
)

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

query = "What is a process?"

embedding = model.encode([query])

results = collection.query(
    query_embeddings=embedding.tolist(),
    n_results=3
)

print(results["documents"][0])