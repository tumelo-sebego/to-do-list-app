from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/save_todo', methods=['POST'])
def save_todo():
    todos = request.form.get('todos', '')
    try:
        with open('todos.txt', 'w', encoding='utf-8') as f:
            f.write(todos)
        return 'success', 200
    except Exception as e:
        return 'error', 400

@app.route('/todos.txt', methods=['GET'])
def get_todos():
    if os.path.exists('todos.txt'):
        with open('todos.txt', 'r', encoding='utf-8') as f:
            return f.read(), 200, {'Content-Type': 'text/plain'}
    else:
        return '', 200, {'Content-Type': 'text/plain'}

if __name__ == '__main__':
    app.run(debug=True)
