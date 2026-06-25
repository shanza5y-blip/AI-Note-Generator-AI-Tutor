from ingest import ingest_file

parsed_structure = {
    "subject": "Operating Systems",

    "units": [

        {
            "unit_name": "Processes",

            "content":
            """
            A process is a program in execution.
            It contains memory, CPU state,
            and system resources.
            """ * 100
        }
    ]
}

ingest_file(
    "file001",
    parsed_structure
)