import chromadb
import ollama
from prompt_templates import PROMPTS

# -----------------------------
# ChromaDB Connection
# -----------------------------

client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_collection(
    "notes_chunks"
)

# -----------------------------
# Retrieve Chunks
# -----------------------------

def retrieve_chunks(file_id,module_name):

    try:
        results = collection.query(
            query_texts=["Generate notes"],
            n_results=5,
            where={"$and": [
            {"file_id": file_id},
            {"module_name": module_name}]}
        )

        docs = results.get("documents", [[]])[0]
        return docs[:5]

    except Exception as e:
        print("Retrieval Error:", e)
        return []

# -----------------------------
# Grounding Check
# -----------------------------

def grounding_check(chunks):

    total_chars = sum(len(chunk) for chunk in chunks)

    if len(chunks) < 2:
        return True

    if total_chars < 200:
        return True

    return False

# -----------------------------
# Ollama Call
# -----------------------------

def call_ollama(prompt):

    response = ollama.chat(
        model="qwen2.5-coder:7b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]

# -----------------------------
# Generate Notes (FIXED)
# -----------------------------

def generate_notes(file_id,module_name, note_type):

    print("\n[STEP] Retrieving chunks...")

    chunks = retrieve_chunks(file_id,module_name)

    print("Retrieved Chunks:", len(chunks))

    # No chunks found
    if len(chunks) == 0:
        return {
            "content": "",
            "warning": f"No content found for file_id='{file_id}' and module_name='{module_name}'"
        }

    context = "\n\n".join(chunks)

    print("[STEP] Building prompt...")

    prompt = PROMPTS["detailed explanation"].format(
        module_name=module_name,
        context=context
    )

    print("[STEP] Calling LLM...")

    notes = call_ollama(prompt)

    result = {
        "content": notes,
        "warning": None
    }

    if grounding_check(chunks):
        result["warning"] = "Low context — syllabus content for this unit may be sparse."

    return result

# -----------------------------
# Direct Test
# -----------------------------

if __name__ == "__main__":

    result = generate_notes(
        "syllabus_001",
        "module 4",
        "detailed"
    )

    print("\nWARNING:")
    print(result["warning"])

    print("\nCONTENT:")
    print(result["content"])