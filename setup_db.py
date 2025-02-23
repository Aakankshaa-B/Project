import sqlite3

conn = sqlite3.connect("schemes.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS schemes (
    id INTEGER PRIMARY KEY,
    name TEXT,
    age_limit INTEGER,
    income_limit INTEGER,
    occupation TEXT ,
    link TEXT
               

)
""")

# Insert sample schemes
cursor.executemany("""
INSERT INTO schemes (name, age_limit, income_limit, occupation) VALUES (?, ?, ?, ?)
""", [
    ("Student Scholarship", 25, 500000, "Student"),
    ("Farmer Loan Subsidy", 50, 700000, "Farmer"),
    ("Small Business Grant", 60, 1000000, "Self-Employed")
])

conn.commit()
conn.close()

print("Database setup completed!")
