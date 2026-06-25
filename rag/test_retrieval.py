import chromadb
from sentence_transformers import SentenceTransformer

# Initialize once
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection("notes_chunks")

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def retrieve(query, k=3):
    emb = model.encode([query])

    result = collection.query(
        query_embeddings=emb.tolist(),
        n_results=k
    )

    return result["documents"][0]


def test_retrieval():

    test_cases = [
        {
            "question": "What is RAG?",
            "expected_keywords": ["retrieval", "generation", "augmented"]
        },
        {
            "question": "What is the objective of the course?",
            "expected_keywords": ["objective", "goal", "aim"]
        },
        {
            "question": "What are evaluation methods?",
            "expected_keywords": ["exam", "marks", "assessment", "evaluation"]
        }
    ]

    correct = 0

    for case in test_cases:
        query = case["question"]
        expected = case["expected_keywords"]

        chunks = retrieve(query, k=3)

        hit = any(
            any(k.lower() in chunk.lower() for k in expected)
            for chunk in chunks
        )

        print("\nQ:", query)
        print("PASS:", hit)

        if hit:
            correct += 1

    score = (correct / len(test_cases)) * 100

    print("\nFINAL SCORE:", score)


if __name__ == "__main__":
    test_retrieval()