import chromadb
from sentence_transformers import SentenceTransformer

client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    name="notes_chunks"
)

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)


def embed_and_store(
    chunks,
    file_id,
    subject,
    unit_name
):

    embeddings = model.encode(chunks)

    ids = []

    metadatas = []

    for i in range(len(chunks)):
        ids.append(f"{file_id}_{i}")

        metadatas.append(
            {
                "file_id": file_id,
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

    print("Chunks stored successfully")