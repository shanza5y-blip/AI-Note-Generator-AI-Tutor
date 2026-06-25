import chromadb
from sentence_transformers import SentenceTransformer
import ollama

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection("notes_chunks")


def retrieve(question):
    emb = model.encode([question])

    results = collection.query(
        query_embeddings=emb.tolist(),
        n_results=2
    )

    docs = results["documents"][0]

    return "\n\n".join(docs)


def answer(question):
    context = retrieve(question)

    prompt = f"""
Answer ONLY using the provided context.

Context:
{context}

Question:
{question}

Answer:
"""

    response = ollama.chat(
        model="llama3.1:8b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]


questions = [
    "What textbook is required for this course?",
    "What percentage is the final examination worth?",
    "What topics are covered in Unit 5?"
]

for q in questions:
    print("\nQUESTION:", q)
    print("\nANSWER:")
    print(answer(q))