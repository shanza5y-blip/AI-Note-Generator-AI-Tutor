from vector_store import get_embedding, query_chunks
import requests

# -----------------------------
# LLM CALL (Ollama)
# -----------------------------
def call_llm(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.1:8b",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]


# -----------------------------
# MAIN RAG FUNCTION
# -----------------------------
def answer_question(question, file_id):

    print("\n[STEP 1] Creating embedding for question...")

    question_embedding = get_embedding(question)

    print("[STEP 2] Retrieving relevant chunks...")

    chunks = query_chunks(
        question_embedding,
        file_id=file_id
    )

    if not chunks:
        return "No relevant context found in database."

    print("[STEP 3] Building prompt...")

    context = "\n\n".join(chunks)

    prompt = f"""
You are an AI tutor.

Use ONLY the context below to answer the question.

Context:
{context}

Question:
{question}

If the answer is not present in the context, reply:
'I couldn't find that information in the uploaded syllabus.'

Answer clearly.
"""

    print("[STEP 4] Generating answer...")

    answer = call_llm(prompt)

    print("[SUCCESS] Answer generated")

    return answer