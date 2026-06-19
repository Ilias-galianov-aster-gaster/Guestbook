import sqlite3
from datetime import date

DATABASE = 'guestbook.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# ---------- Получение сообщений с сортировкой (задание А) ----------
def get_all_messages(order='DESC'):
    """
    Возвращает все сообщения.
    order: 'DESC' (новые сверху) или 'ASC' (старые сверху)
    """
    conn = get_db_connection()
    query = f'SELECT * FROM messages ORDER BY created_at {order}, id {order}'
    messages = conn.execute(query).fetchall()
    conn.close()
    return messages

# ---------- Добавление ----------
def add_message(name, message):
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO messages (name, message, created_at) VALUES (?, ?, ?)',
        (name, message, date.today().strftime('%Y-%m-%d'))
    )
    conn.commit()
    conn.close()

# ---------- Удаление одного (задание 1) ----------
def delete_message(message_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM messages WHERE id = ?', (message_id,))
    conn.commit()
    conn.close()

# ---------- Счётчик (задание 5) ----------
def get_message_count():
    conn = get_db_connection()
    cursor = conn.execute('SELECT COUNT(*) FROM messages')
    count = cursor.fetchone()[0]
    conn.close()
    return count

# ---------- Удаление всех (задание В) ----------
def delete_all_messages():
    conn = get_db_connection()
    conn.execute('DELETE FROM messages')
    conn.commit()
    conn.close()