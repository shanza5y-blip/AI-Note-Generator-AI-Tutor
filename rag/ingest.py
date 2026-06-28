import uuid
from parser import extract_pdf_text
from chunker import chunk_text
from vector_store import add_documents


COLLECTION_NAME = "notes_chunks"


def ingest_file(file_id, parsed_structure):
    subject = parsed_structure["subject"]
    modules = parsed_structure["modules"]

    all_texts = []
    all_metadatas = []

    for module in modules:
        module_name = module["module_name"]

        for topic in module["topics"]:

            # FIX 1: better chunking (each topic becomes a chunk)
            all_texts.append(f"{topic} is a topic in {module_name} of {subject}. It covers key concepts in Computer Networks."
)

            all_metadatas.append({
                "file_id": file_id,
                "subject": subject,
                "module_name": module_name,
                "topic": topic
            })

    # FIX 2: single batch insert (faster + safer)
    add_documents(
        texts=all_texts,
        metadatas=all_metadatas,
        collection_name=COLLECTION_NAME
    )

    print("Ingestion Complete")


def ingest_pdf(file_path: str) -> str:
    file_id = str(uuid.uuid4())

    text = extract_pdf_text(file_path)
    chunks = chunk_text(text)

    # FIX 3: consistent metadata (IMPORTANT)
    add_documents(
        texts=chunks,
        metadatas=[
            {
                "file_id": file_id,
                "subject": "Unknown",
                "module_name": "Unknown",
                "topic": "Unknown"
            }
            for _ in chunks
        ],
        collection_name=COLLECTION_NAME
    )

    return file_id


if __name__ == "__main__":

    parsed = {
        "subject": "Computer Networks",
        "modules": [
            {
                "module_name": "Module 4",
                "topics": [
                    "Routing Algorithms",
                    "Distance Vector Routing",
                    "Link State Routing"
                ]
            }
        ]
    }

    ingest_file("syllabus_001", parsed)