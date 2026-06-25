import os
import chromadb
from sentence_transformers import SentenceTransformer

# --------------------------------------------------
# Create local cache folders
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

HF_CACHE_DIR = os.path.join(BASE_DIR, "hf_cache")
CHROMA_DB_DIR = os.path.join(BASE_DIR, "chroma_db")

os.makedirs(HF_CACHE_DIR, exist_ok=True)
os.makedirs(CHROMA_DB_DIR, exist_ok=True)

# Tell HuggingFace to use local cache
os.environ["HF_HOME"] = HF_CACHE_DIR
os.environ["HUGGINGFACE_HUB_CACHE"] = HF_CACHE_DIR
os.environ["TRANSFORMERS_CACHE"] = HF_CACHE_DIR

# --------------------------------------------------
# ChromaDB
# --------------------------------------------------

client = chromadb.PersistentClient(
    path=CHROMA_DB_DIR
)

collection = client.get_or_create_collection(
    name="notes_chunks"
)

# --------------------------------------------------
# Embedding Model
# --------------------------------------------------

print("Loading embedding model...")

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2",
    cache_folder=HF_CACHE_DIR
)

print("Embedding model loaded successfully.")

# --------------------------------------------------
# Store Chunks
# --------------------------------------------------

def embed_and_store(
    chunks,
    file_id,
    subject,
    unit_name
):
    try:

        if not chunks:
            print("No chunks found.")
            return

        embeddings = model.encode(
            chunks,
            show_progress_bar=False
        )

        ids = []
        metadatas = []

        for i, chunk in enumerate(chunks):

            ids.append(f"{file_id}_{unit_name}_{i}")

            metadatas.append(
                {
                    "file_id": str(file_id),
                    "subject": subject,
                    "unit_name": unit_name,
                    "chunk_index": i
                }
            )

        collection.upsert(
            ids=ids,
            documents=chunks,
            embeddings=embeddings.tolist(),
            metadatas=metadatas
        )

        print(
            f"Stored {len(chunks)} chunks for "
            f"{subject} -> {unit_name}"
        )

    except Exception as e:

        print(
            f"Error storing embeddings: {e}"
        )