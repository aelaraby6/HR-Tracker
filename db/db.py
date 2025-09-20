import sqlite3
from contextlib import closing

DB_NAME = "database.db"


# ========== Users ==========
def add_user(username, telegram_id, full_name):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, telegram_id, full_name) VALUES (?, ?, ?)",
            (username, telegram_id, full_name),
        )
        conn.commit()

def get_user_by_id(user_id):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        return cursor.fetchone()

def get_all_users():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        return cursor.fetchall()

def update_user(user_id, username=None, telegram_id=None, full_name=None):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        if username:
            cursor.execute(
                "UPDATE users SET username = ? WHERE user_id = ?",
                (username, user_id),
            )
        if telegram_id:
            cursor.execute(
                "UPDATE users SET telegram_id = ? WHERE user_id = ?",
                (telegram_id, user_id),
            )
        if full_name:
            cursor.execute(
                "UPDATE users SET full_name = ? WHERE user_id = ?",
                (full_name, user_id),
            )
        conn.commit()

def delete_user(user_id):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        conn.commit()
