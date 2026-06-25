import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
ALTER TABLE files
ADD COLUMN parsed_json TEXT
""")

conn.commit()
conn.close()

print("parsed_json column added successfully")