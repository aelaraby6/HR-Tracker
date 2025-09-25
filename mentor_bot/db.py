
import sqlite3

DB_NAME = "mentor_bot.db"  

def get_connection():
   
    return sqlite3.connect(DB_NAME)

def create_tables():
    
    conn = get_connection()
    cursor = conn.cursor()

    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS groups (
        group_id INTEGER PRIMARY KEY,
        group_name TEXT NOT NULL,
        telegram_id TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')

  
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        full_name TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'mentor',
        group_id INTEGER,
        FOREIGN KEY (group_id) REFERENCES groups (group_id)
    )
    ''')

 
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        message_id INTEGER PRIMARY KEY,
        group_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        message_text TEXT NOT NULL,
        sent_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (group_id) REFERENCES groups (group_id),
        FOREIGN KEY (user_id) REFERENCES users (user_id)
    )
    ''')

   
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS reports (
        report_id INTEGER PRIMARY KEY,
        group_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        start_date DATETIME NOT NULL,
        end_date DATETIME NOT NULL,
        export_path TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (group_id) REFERENCES groups (group_id),
        FOREIGN KEY (user_id) REFERENCES users (user_id)
    )
    ''')

    conn.commit()
    conn.close()


def add_group(group_id, group_name, telegram_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
        INSERT OR REPLACE INTO groups (group_id, group_name, telegram_id)
        VALUES (?, ?, ?)
        ''', (group_id, group_name, telegram_id))
        conn.commit()
    finally:
        conn.close()

def add_mentor(user_id, username, full_name, group_id=None):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
        INSERT OR REPLACE INTO users (user_id, username, full_name, role, group_id)
        VALUES (?, ?, ?, 'mentor', ?)
        ''', (user_id, username, full_name, group_id))
        conn.commit()
    finally:
        conn.close()


def get_all_groups():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM groups")
    groups = cursor.fetchall()
    conn.close()
    return groups

def get_all_mentors():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE role = 'mentor'")
    mentors = cursor.fetchall()
    conn.close()
    return mentors

def get_mentors_for_group(group_name):
   
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT u.full_name
        FROM users u
        JOIN groups g ON u.group_id = g.group_id
        WHERE LOWER(g.group_name) LIKE LOWER(?)
        AND u.role = 'mentor'
    """, (f"%{group_name}%",))
    mentors = [row[0] for row in cursor.fetchall()]
    conn.close()
    return mentors

def get_mentor_by_name(name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE full_name LIKE ?", (f"%{name}%",))
    mentors = cursor.fetchall()
    conn.close()
    return mentors

def get_group_by_name(name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM groups WHERE group_name LIKE ?", (f"%{name}%",))
    group = cursor.fetchone()
    conn.close()
    return group
