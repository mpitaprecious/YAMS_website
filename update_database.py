import sqlite3


conn = sqlite3.connect('database.db')
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE applications ADD COLUMN status TEXT DEFAULT 'Pending'")
except:
    print("status column already exists")
try:
    cursor.execute("ALTER TABLE applications ADD COLUMN archived INTEGER DEFAULT 0")
except:
    print("archived column already exists")

try:
    cursor.execute("ALTER TABLE applications ADD COLUMN completed_date TEXT")
except:
    print("completed_date column exists")

conn.commit()
conn.close()

print("Database updated successfully!")
