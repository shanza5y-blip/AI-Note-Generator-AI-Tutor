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

def retrieve_chunks(file_id, unit_name):

    try:
        results = collection.get(
            where={
                "$and": [
                    {"file_id": file_id},
                    {"unit_name": unit_name}
                ]
            }
        )

        docs = results.get("documents", [])

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
# Generate Notes
# -----------------------------

def generate_notes(
    file_id,
    unit_name,
    note_type
):

    chunks = retrieve_chunks(
        file_id,
        unit_name
    )

    print("\nRetrieved Chunks:", len(chunks))

    # No chunks found
    if len(chunks) == 0:
        return {
            "content": "",
            "warning": (
                f"No content found for "
                f"file_id='{file_id}' "
                f"and unit_name='{unit_name}'"
            )
        }

    context = "\n\n".join(chunks)

    prompt = PROMPTS[note_type].format(
        unit_name=unit_name,
        context=context
    )

    notes = call_ollama(prompt)

    result = {
        "content": notes,
        "warning": None
    }

    if grounding_check(chunks):
        result["warning"] = (
            "Low context — syllabus content "
            "for this unit may be sparse."
        )

    return result


# -----------------------------
# Direct Test
# -----------------------------

if __name__ == "__main__":

    result = generate_notes(
        file_id="syllabus_001",
        unit_name="Course Syllabus",
        note_type="detailed"
    )

    print("\nWARNING:")
    print(result["warning"])

    print("\nCONTENT:")
    print(result["content"])