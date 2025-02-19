import sqlite3

conn = sqlite3.connect('database.db')  
cursor = conn.cursor()

# Insert a new admin (change 'newadmin' and 'newpassword' as needed)
cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('Muhammad', 'MuhammadAdmin'))
conn.commit()
conn.close()

print("New admin added successfully!")
