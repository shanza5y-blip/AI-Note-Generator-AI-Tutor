from chunker import chunk_text
from vector_store import embed_and_store


def ingest_file(file_id, parsed_structure):

    subject = parsed_structure["subject"]

    units = parsed_structure["units"]

    for unit in units:

        unit_name = unit["unit_name"]

        for chapter in unit["chapters"]:

            chunks = chunk_text(chapter)

            embed_and_store(
                chunks,
                file_id,
                subject,
                unit_name
            )

    print("Ingestion Complete")