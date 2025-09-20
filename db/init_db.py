import sqlite3

conn = sqlite3.connect('db')
cursor = conn.cursor()


#Users
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    telegram_id TEXT NOT NULL,
    full_name TEXT NOT NULL
)
''')


conn.commit()
conn.close()

print("Done")