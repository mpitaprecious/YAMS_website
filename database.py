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

conn.commit()
conn.close()

print("Database created successfully.")