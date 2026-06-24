from PyPDF2 import PdfReader
import re


def extract_pdf_text(file_path):

    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return {
        "text": text,
        "page_count": len(reader.pages)
    }


def parse_syllabus(text):

    subject = "Unknown Subject"

    match = re.search(
        r"COURSE NAME:\s*(.+)",
        text,
        re.IGNORECASE
    )

    if match:
        subject = match.group(1).strip()

    # Extract only syllabus section
    syllabus_match = re.search(
        r"SYLLABUS(.*?)Course Assessment Method",
        text,
        re.DOTALL | re.IGNORECASE
    )

    syllabus_text = syllabus_match.group(1) if syllabus_match else text

    units = []

    module_pattern = (
        r"(?m)^([1-4])\s+(.+?)(?=\n[1-4]\s+|\Z)"
    )

    modules = re.findall(
        module_pattern,
        syllabus_text,
        re.DOTALL
    )

    for module_no, content in modules:

        title = content.split("[Text")[0].strip()

        units.append({
            "unit_name": f"Module {module_no}",
            "chapters": [title]
        })

    return {
        "subject": subject,
        "units": units
    }
