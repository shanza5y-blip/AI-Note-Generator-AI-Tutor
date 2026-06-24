from utils.pdf_parser import extract_pdf_text

result = extract_pdf_text(
    "uploads/sample.pdf"
)

print(result["page_count"])
print(result["text"][:500])
