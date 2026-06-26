from vector_store import add_documents, get_embedding, query_chunks

# -----------------------------
# SAMPLE DATA (fake RAG input)
# -----------------------------
texts = [
    "AI is smart and learns from data",
    "RAG helps LLMs use external knowledge",
    "Python is widely used in AI projects"
]

metadatas = [
    {"file_id": "test1", "subject": "ai", " module_name ": "intro"},
    {"file_id": "test1", "subject": "ai", " module_name ": "intro"},
    {"file_id": "test1", "subject": "ai", " module_name ": "intro"}
]

# -----------------------------
# STEP 1: STORE DATA IN CHROMA
# -----------------------------
print("\n[STEP 1] Adding documents to vector DB...")
add_documents(texts, metadatas, "notes_chunks")

# -----------------------------
# STEP 2: CREATE QUERY EMBEDDING
# -----------------------------
print("\n[STEP 2] Creating embedding...")
emb = get_embedding("what is AI?")

# -----------------------------
# STEP 3: RETRIEVE SIMILAR CHUNKS
# -----------------------------
print("\n[STEP 3] Querying vector DB...")
result = query_chunks(emb)

# -----------------------------
# OUTPUT RESULT
# -----------------------------
print("\n================ RESULT ================\n")
print(result)
print("\n========================================\n")