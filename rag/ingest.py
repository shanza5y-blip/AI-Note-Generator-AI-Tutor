import uuid
from backend.parser import extract_pdf_text
from rag.chunker import chunk_text
from rag.vector_store import add_documents


def ingest_file(file_id, parsed_structure):
    subject = parsed_structure["subject"]
    modules = parsed_structure["modules"]

    for module in modules:
        module_name = module["module_name"]

        for topic in module["topics"]:
            chunks = [topic]

            add_documents(
                texts=chunks,
                metadatas=[{
                    "file_id": file_id,
                    "subject": subject,
                    "module_name": module_name
                } for _ in chunks],
                collection_name=file_id
            )

    print("Ingestion Complete")


def ingest_pdf(file_path: str) -> str:
    file_id = str(uuid.uuid4())

    text = extract_text(file_path)
    chunks = chunk_text(text)

    add_documents(
        texts=chunks,
        metadatas=[{"file_id": file_id} for _ in chunks],
        collection_name=file_id
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

    ingest_file(
        "syllabus_001",
        parsed
    )