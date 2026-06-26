from ingest import ingest_file

def test_ingestion_runs():

    parsed_structure = {

        "subject": "AI",

        "units": [
            {
                "module_name": "RAG",

                "content":
                "Retrieval Augmented Generation." * 100
            }
        ]
    }

    ingest_file(
        "test_file",
        parsed_structure
    )

    assert True