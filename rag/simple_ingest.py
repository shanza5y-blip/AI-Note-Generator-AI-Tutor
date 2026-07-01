from chunker import chunk_text
from vector_store import add_documents

file_id = "syllabus_001"

units = {
    "Unit 1": "Introduction to Artificial Intelligence...",
    "Unit 2": "Machine Learning Fundamentals...",
    "Unit 3": "Neural Networks and Deep Learning...",
    "Unit 4": "Vector Databases and Embeddings...",
    "Unit 5": "Retrieval Augmented Generation...",
    "Unit 6": "Prompt Engineering..."
}

for unit_name, content in units.items():

    chunks = chunk_text(content)

    add_documents(
        texts=chunks,
        metadatas=[
            {
                "file_id": file_id,
                "module_name": module_name,
                "subject": "AI"
            }
            for _ in chunks
        ],
        collection_name="notes_chunks"
    )

print("INGESTION COMPLETE")