import chromadb

def test_chroma_connection():

    client = chromadb.PersistentClient(
        path="./chroma_db"
    )

    collection = client.get_or_create_collection(
        "test_collection"
    )

    assert collection.name == "test_collection"