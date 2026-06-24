import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("DELETE FROM files")

# Reset auto-increment counter
cursor.execute("DELETE FROM sqlite_sequence WHERE name='files'")

conn.commit()
conn.close()

print("Database cleared successfully")
