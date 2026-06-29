import uuid
import json
from parser import extract_pdf_text, parse_syllabus
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
            text = f"{module_name} | {topic} | {subject}"

            all_texts.append(text)
            all_metadatas.append({
                "file_id": file_id,
                "subject": subject,
                "module_name": module_name,
                "topic": topic
            })
    print("\n===== METADATA =====")
    for m in all_metadatas:
        print(m)
    add_documents(
        texts=all_texts,
        metadatas=all_metadatas,
        collection_name=COLLECTION_NAME
    )

    print("[SUCCESS] Ingestion Complete")


def ingest_pdf(file_path: str):
    file_id = str(uuid.uuid4())

    text = extract_pdf_text(file_path)
    parsed = parse_syllabus(text)

    ingest_file(file_id, parsed)

    print(json.dumps(parsed, indent=2))


if __name__ == "__main__":
    file_path = r"C:\Users\Jumana\OneDrive\project\rag\Syllabus.pdf"
    ingest_pdf(file_path)