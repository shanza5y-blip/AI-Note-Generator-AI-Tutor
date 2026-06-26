import chromadb
from sentence_transformers import SentenceTransformer
import hashlib

# -----------------------------
# ChromaDB Setup
# -----------------------------

client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    name="notes_chunks"
)

# -----------------------------
# Embedding Model
# -----------------------------

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

# -----------------------------
# Helper: Create Unique ID
# -----------------------------

def create_id(file_id, module_name, chunk_text, index):
    hash_val = hashlib.md5(chunk_text.encode()).hexdigest()[:8]
    return f"{file_id}_{module_name}_{index}_{hash_val}"

# -----------------------------
# Store Chunks
# -----------------------------

def embed_and_store(
    chunks,
    file_id,
    subject,
    module_name
):
    print("\n[INFO] Embedding chunks...")

    embeddings = model.encode(chunks)

    ids = []
    metadatas = []

    for i, chunk in enumerate(chunks):

        ids.append(
            create_id(file_id, module_name, chunk, i)
        )

        metadatas.append({
            "file_id": file_id,
            "subject": subject,
            "module_name": module_name,
            "chunk_index": i
        })

    collection.upsert(
        ids=ids,
        documents=chunks,
        embeddings=embeddings.tolist(),
        metadatas=metadatas
    )

    print(f"[SUCCESS] Stored {len(chunks)} chunks")

# -----------------------------
# Compatibility Wrapper
# -----------------------------

def add_documents(texts, metadatas, collection_name=None):
    """
    Wrapper for ingest.py
    """

    if not metadatas:
        return

    embed_and_store(
        chunks=texts,
        file_id=metadatas[0]["file_id"],
        subject=metadatas[0].get("subject", "unknown"),
        module_name=metadatas[0].get("module_name", "unknown")
    )

# -----------------------------
# Embedding Helper
# -----------------------------

def get_embedding(text):
    return model.encode(text).tolist()

# -----------------------------
# Retrieve Chunks
# -----------------------------

def query_chunks(question_embedding, file_id, top_k=3):

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=top_k,
        where={
            "file_id": file_id
        }
    )

    return results["documents"][0]
    """
    Retrieve top matching chunks.
    """

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=top_k
    )

    return results["documents"][0]

# -----------------------------
# Debug Helper
# -----------------------------

def debug_collection():
    print("\nTotal Chunks:", collection.count())

    sample = collection.get(limit=5)

    print(sample)