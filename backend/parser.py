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

    modules = []

    module_pattern = (
        r"(?ms)^\s*([1-4])\s+(.+?)(?=^\s*[1-4]\s+|\Z)"
    )

    matches = re.findall(
        module_pattern,
        syllabus_text,
        re.MULTILINE | re.DOTALL
    )
    print("Modules found:", len(matches))

    for m in matches:
        print(m[0], "->", m[1][:80])

    for module_no, content in matches:

        title = content.split("[Text")[0].strip()

        modules.append({
            "module_name": f"Module {module_no}",
            "topics": [title]
        })

    return {
        "subject": subject,
        "modules": modules
    }
