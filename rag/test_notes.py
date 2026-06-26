from note_generator import generate_notes

result = generate_notes(
    file_id="syllabus_001",
    module_name ="module 4",
    note_type="detailed explanation"
)

print("\nWARNING:")
print(result["warning"])

print("\nCONTENT:")
print(result["content"])