from flask import Flask, request, send_from_directory, jsonify
import os
import sqlite3

app = Flask(__name__)

DB_PATH = 'todos.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            completed BOOLEAN NOT NULL DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    # Serve the HTML frontend (from index.html)
    with open('index.html', 'r', encoding='utf-8') as f:
        return f.read()

@app.route('/app.js')
def app_js():
    return send_from_directory('.', 'app.js')

@app.route('/style.css')
def style_css():
    return send_from_directory('.', 'style.css')

@app.route('/save_todo', methods=['POST'])
def save_todo():
    # Expects 'todos' as a string: text|completed\ntext|completed...
    todos_raw = request.form.get('todos', '')
    todos = []
    for line in todos_raw.strip().split('\n'):
        if '|' in line:
            text, completed = line.rsplit('|', 1)
            todos.append((text, completed.lower() == 'true'))

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('DELETE FROM todos')
    c.executemany('INSERT INTO todos (text, completed) VALUES (?, ?)', todos)
    conn.commit()
    conn.close()
    return 'success', 200

@app.route('/todos', methods=['GET'])
def get_todos():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT text, completed FROM todos')
    rows = c.fetchall()
    conn.close()
    # Return in the same format as before: text|completed\n...
    todos_txt = '\n'.join(f"{text}|{str(bool(completed)).lower()}" for text, completed in rows)
    return todos_txt, 200, {'Content-Type': 'text/plain'}

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
