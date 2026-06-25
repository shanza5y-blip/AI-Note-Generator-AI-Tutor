import chromadb
from sentence_transformers import SentenceTransformer

text = """
RAG combines retrieval and generation.

Chunking divides documents into smaller sections.

Embeddings convert text into vectors.
"""

chunks = [
    p.strip()
    for p in text.split("\n")
    if p.strip()
]

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

embeddings = model.encode(chunks)

client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    name="notes_chunks"
)

collection.add(
    ids=[f"id_{i}" for i in range(len(chunks))],
    documents=chunks,
    embeddings=embeddings.tolist()
)

query = "What are embeddings?"

query_embedding = model.encode([query])

results = collection.query(
    query_embeddings=query_embedding.tolist(),
    n_results=2
)

print("\nQuery:")
print(query)

print("\nResults:")

for item in results["documents"][0]:
    print("-", item)