import chromadb
from sentence_transformers import SentenceTransformer
from test_questions import TEST_CASES

# Load embedding model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Connect to ChromaDB
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection("notes_chunks")


def retrieve(query):
    """
    Retrieve the top matching document chunk.
    """
    emb = model.encode([query])

    results = collection.query(
        query_embeddings=emb.tolist(),
        n_results=1
    )

    documents = results.get("documents", [])

    if not documents or not documents[0]:
        return ""

    return documents[0][0]


def evaluate():
    correct = 0
    total = len(TEST_CASES)

    report = []

    for case in TEST_CASES:
        query = case["question"]
        expected = case["expected_keywords"]

        chunk = retrieve(query)

        hit = any(
            keyword.lower() in chunk.lower()
            for keyword in expected
        )

        print("\n" + "=" * 60)
        print("QUESTION:", query)

        print("\nRetrieved Chunk:")
        print(chunk[:500] if chunk else "No chunk returned")

        print("\nPASS:", hit)

        report.append({
            "question": query,
            "retrieved_chunk": chunk[:300] if chunk else "",
            "passed": hit
        })

        if hit:
            correct += 1

    score = (correct / total * 100) if total > 0 else 0

    return score, report


if __name__ == "__main__":
    score, report = evaluate()

    print("\n" + "=" * 60)
    print("Retrieval Score:", score, "%")

    for r in report:
        print("\nQ:", r["question"])
        print("PASS:", r["passed"])