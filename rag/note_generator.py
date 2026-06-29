import chromadb
import ollama
from prompt_templates import PROMPTS

# -----------------------------
# ChromaDB Connection
# -----------------------------

client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_collection("notes_chunks")


# -----------------------------
# Retrieve Chunks
# -----------------------------

def retrieve_chunks(file_id, module_name):

    try:
        print("\n===== RETRIEVING =====")
        print("file_id:", file_id, type(file_id))
        print("module_name:", module_name)

        results = collection.get(
            where={
                "$and": [
                    {"file_id": file_id},
                    {"module_name": module_name}
                ]
            },
            include=["documents", "metadatas"]
        )

        docs = results.get("documents", [])

        print("\nRetrieved Documents:", len(docs))

        if docs:
            print("\nMetadata:")
            for meta in results["metadatas"]:
                print(meta)

        return docs

    except Exception as e:
        print("Retrieval Error:", e)
        return []


# -----------------------------
# Grounding Check
# -----------------------------

def grounding_check(chunks):

    keywords = [
        "routing",
        "network",
        "algorithm"
    ]

    score = 0

    for chunk in chunks:
        if any(k in chunk.lower() for k in keywords):
            score += 1

    return score < 2


# -----------------------------
# Ollama
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

def generate_notes(file_id, module_name, note_type):

    print("\n==============================")
    print("Generating Notes")
    print("==============================")

    chunks = retrieve_chunks(file_id, module_name)

    if len(chunks) == 0:
        return {
            "content": "",
            "warning": f"No content found for file_id='{file_id}' and module_name='{module_name}'"
        }

    context = "\n\n".join(chunks)

    print("\n===== CONTEXT =====")
    print(context[:1000])

    prompt = PROMPTS["detailed explanation"].format(
        module_name=module_name,
        context=context
    )

    notes = call_ollama(prompt)

    result = {
        "content": notes,
        "warning": None
    }

    if grounding_check(chunks):
        result["warning"] = "Low context — syllabus content for this unit may be sparse."

    return result


# -----------------------------
# Test
# -----------------------------

if __name__ == "__main__":

    result = generate_notes(
        1,
        "Module 2",
        "detailed"
    )

    print(result)