import sqlite3

def get_connection():
    return sqlite3.connect('mentor_bot.db')

def add_mentor(user_id, username, full_name):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
        INSERT INTO users (user_id, username, full_name)
        VALUES (?, ?, ?)
        ''', (user_id, username, full_name))
        conn.commit()
        print(f"Added mentor {full_name} successfully!")
        return True
    except Exception as e:
        print(f"Error adding mentor: {e}")
        return False
    finally:
        conn.close()

def add_group(group_id, group_name, telegram_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
        INSERT INTO groups (group_id, group_name, telegram_id)
        VALUES (?, ?, ?)
        ''', (group_id, group_name, telegram_id))
        conn.commit()
        print(f"Added group {group_name} successfully!")
        return True
    except Exception as e:
        print(f"Error adding group: {e}")
        return False
    finally:
        conn.close()

def get_all_mentors():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM users')
        mentors = cursor.fetchall()
        return mentors
    except Exception as e:
        print(f"Error getting mentors: {e}")
        return []
    finally:
        conn.close()

def get_all_groups():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM groups')
        groups = cursor.fetchall()
        return groups
    except Exception as e:
        print(f"Error getting groups: {e}")
        return []
    finally:
        conn.close()