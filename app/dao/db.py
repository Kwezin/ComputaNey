import sqlite3
import os

DB_PATH = "/tmp/users.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            cpf TEXT,
            email TEXT UNIQUE,
            tipo TEXT,
            tags TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_user(nome, cpf, email, tipo, tags):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO usuarios (nome, cpf, email, tipo, tags) VALUES (?, ?, ?, ?, ?)",
        (nome, cpf, email, tipo, ",".join(tags))
    )
    conn.commit()
    conn.close()

def get_user(email):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM usuarios WHERE email=?", (email,))
    user = cur.fetchone()
    conn.close()
    return user
