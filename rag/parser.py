from PyPDF2 import PdfReader
import re

def extract_pdf_text(file_path: str) -> str:
    from PyPDF2 import PdfReader

    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        t = page.extract_text()
        if t:
            text += t + "\n"

    return text


def parse_syllabus(text: str):
    lines = [l.strip() for l in text.split("\n") if l.strip()]

    modules = []
    current = None

    def is_module_line(line):
        # matches: "1 Introduction", "2 Euler Graphs", etc.
        return re.match(r"^\d+\s+[A-Za-z]", line)

    for line in lines:

        # detect module start
        if is_module_line(line):
            parts = line.split(" ", 1)

            module_number = parts[0]
            title = parts[1] if len(parts) > 1 else ""

            current = {
                "module_name": f"Module {module_number}",
                "topics": [title]
            }
            modules.append(current)

        elif current:
            current["topics"].append(line)

    return {
        "subject": "Computer Networks",
        "modules": modules
    }