import uuid
import json
from parser import extract_pdf_text, parse_syllabus
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

            all_texts.append(
                f"{topic} is a topic in {module_name} of {subject}. It covers key concepts in Computer Networks."
            )

            all_metadatas.append({
                "file_id": file_id,
                "subject": subject,
                "module_name": module_name,
                "topic": topic
            })

    add_documents(
        texts=all_texts,
        metadatas=all_metadatas,
        collection_name=COLLECTION_NAME
    )

    print("Ingestion Complete")


def ingest_pdf(file_path: str) -> str:
    file_id = str(uuid.uuid4())

    # STEP 1: Extract text
    text = extract_pdf_text(file_path)

    # STEP 2: Convert text → structured syllabus
    parsed = parse_syllabus(text)

    # STEP 3: Ingest structured data
    ingest_file(file_id, parsed)

    print(json.dumps(parsed, indent=2))

    return file_id


if __name__ == "__main__":
    file_path = r"C:\Users\Jumana\OneDrive\project\rag\Syllabus.pdf"

    ingest_pdf(file_path)