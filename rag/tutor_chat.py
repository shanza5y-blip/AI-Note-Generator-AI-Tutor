from ollama import chat
from rag.vector_store import collection, get_embedding
import json
from rag.tutor_prompts import SYSTEM_PROMPT
from concurrent.futures import ThreadPoolExecutor, TimeoutError


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

Retrieved syllabus context:

{context}

Instructions for answering:

1. Use the retrieved syllabus context as the primary source.
2. If the context only lists the topic or is incomplete, provide a complete explanation using your own academic knowledge.
3. Mention briefly that the syllabus only briefly covers the topic if relevant.
4. Never refuse to answer because the context is incomplete.
5. Give a clear, structured explanation suitable for a university student.
"""

    # 4. Build messages (history is mandatory)
    messages = [
        {"role": "system", "content": system_prompt},
        *history,
        {"role": "user", "content": message}
    ]

    # 5. Call Ollama
    # 5. Call Ollama with 30-second timeout
    try:
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(
                chat,
                model="llama3.1:8b",
                messages=messages
            )

            response = future.result(timeout=30)

    except TimeoutError:
        return {
            "answer": "The AI tutor took longer than 30 seconds to respond. Please try again.",
            "sources": []
        }

    except Exception as e:
        return {
            "answer": "Unable to communicate with the AI tutor. Please try again later.",
            "sources": []
        }

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
