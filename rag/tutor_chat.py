from ollama import chat
from vector_store import collection, get_embedding
import json
from tutor_prompts import SYSTEM_PROMPT


def tutor_chat(
    file_id: str,
    subject: str,
    message: str,
    history: list   # MANDATORY
):
    """
    Returns:
    {
        "answer": "...",
        "sources": [
            {
                "unit_name": "...",
                "chunk_preview": "..."
            }
        ]
    }
    """

    # 1. Embed query
    question_embedding = get_embedding(message)

    # 2. Retrieve syllabus chunks
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=3,
        where={"file_id": file_id},
        include=["documents", "metadatas"]
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    context = ""
    sources = []

    for doc, meta in zip(documents, metadatas):
        module_name = meta.get("module_name", "Unknown Module")

        context += f"\n\nModule: {module_name}\n{doc}"

        sources.append({
            "unit_name": module_name,
            "chunk_preview": doc[:120].strip()
        })

    # 3. Inject syllabus context into system prompt
    system_prompt = SYSTEM_PROMPT + f"""

Syllabus Context:
{context}
"""

    # 4. Build messages (history is mandatory)
    messages = [
        {"role": "system", "content": system_prompt},
        *history,
        {"role": "user", "content": message}
    ]

    # 5. Call Ollama
    response = chat(
        model="llama3.1:8b",
        messages=messages
    )

    return {
        "answer": response["message"]["content"],
        "sources": sources
    }


if __name__ == "__main__":
    response = tutor_chat(
        file_id="syllabus_001",
        subject="Computer Networks",
        message="What is Link State Routing?",
        history=[
            {"role": "user", "content": "Explain routing basics"},
            {"role": "assistant", "content": "Routing is the process of..."}
        ]
    )

    print("\n===== FINAL RESPONSE =====")
    print(json.dumps(response, indent=2))