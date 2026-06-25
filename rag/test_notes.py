from note_generator import generate_notes

result = generate_notes(
    file_id="long_syllabus",
    unit_name="Unit 5",
    note_type="detailed"
)

print("\nWARNING:")
print(result["warning"])

print("\nCONTENT:")
print(result["content"])