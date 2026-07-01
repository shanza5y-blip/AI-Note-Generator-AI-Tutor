import chromadb

TEST_CASES = [

    ("What is RAG?", "retrieval"),

    ("What are embeddings?", "vectors")

]

def test_accuracy():

    client = chromadb.PersistentClient(
        path="./chroma_db"
    )

    collection = client.get_collection(
        "notes_chunks"
    )

    correct = 0

    for question, expected_word in TEST_CASES:

        result = collection.query(
            query_texts=[question],
            n_results=1
        )

        retrieved_text = result["documents"][0][0]

        print("\nQuestion:", question)
        print("Retrieved:", retrieved_text)

        if expected_word.lower() in retrieved_text.lower():
            correct += 1

    accuracy = (
        correct /
        len(TEST_CASES)
    ) * 100

    print("\nAccuracy:", accuracy)

    assert accuracy >= 80