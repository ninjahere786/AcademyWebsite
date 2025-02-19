import sqlite3

# Connect to SQLite database (creates database.db if it doesn't exist)
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create users table (for storing admin credentials)
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
''')

# Create videos table (for storing uploaded video details)
cursor.execute('''
CREATE TABLE IF NOT EXISTS videos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    filename TEXT NOT NULL,
    upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# Insert default admin user
cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('admin', 'admin123'))

# Save changes and close the connection
conn.commit()
conn.close()

print("Database initialized successfully!")
