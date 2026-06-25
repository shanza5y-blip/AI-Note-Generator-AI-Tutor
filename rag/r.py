results = collection.query(
    query_texts=["<any topic from the syllabus she uploaded>"],
    n_results=3,
    include=["documents", "metadatas", "distances"]
)
print(results)