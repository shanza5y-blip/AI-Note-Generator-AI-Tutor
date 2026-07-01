from chunker import chunk_text
from vector_store import embed_and_store

print("1. Opening file...")

with open("long_syllabus.txt", "r", encoding="utf-8") as f:
    text = f.read()

print("2. File loaded")

chunks = chunk_text(text)

print("3. Number of chunks:", len(chunks))

print("4. Calling embed_and_store...")

embed_and_store(
    chunks=chunks,
    file_id="syllabus_001",
    subject="AI",
    module_name="Course Syllabus"
)

print("5. Syllabus stored successfully")