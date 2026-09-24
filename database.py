import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fullname TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT,
    location TEXT NOT NULL,
    service TEXT NOT NULL,
    description TEXT NOT NULL,
    service_date TEXT,
    status TEXT DEFAULT 'Pending'
)
''')


cursor.execute("""ALTER TABLE applications ADD COLUMN latitude REAL
""")
cursor.execute("""ALTER TABLE applications ADD COLUMN longitude REAL
""")

conn.commit()
conn.close()

print("GPS columns added successfully.")
print("Database created successfully.")