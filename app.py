"""
Crie uma aplicação web simples onde os usuários possam gerenciar suas tarefas diárias. 
O sistema permitirá adicionar, visualizar, atualizar e excluir tarefas. Além disso, 
inclua a funcionalidade de marcar uma tarefa como concluída.
"""
from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

# Função para inicializar o banco de dados
def init_db():
    with sqlite3.connect('tasks.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, task TEXT)''')
        conn.commit()

# Rota para exibir a lista de tarefas
@app.route('/')
def index():
    with sqlite3.connect('tasks.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, task FROM tasks')
        tasks = cursor.fetchall()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task = request.form.get('task')
    if task:
        with sqlite3.connect('tasks.db') as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO tasks (task) VALUES (?)', (task,))
            conn.commit()
    return index()

@app.route('/delete/<int:id>')
def delete_task(id):
    with sqlite3.connect('tasks.db') as conn:  # Corrigido para 'tasks.db'
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tasks WHERE id = ?', (id,))
        conn.commit()
    return index()

if __name__ == '__main__':
    init_db()  # Chama a função para garantir que a tabela seja criada
    app.run(debug=True)
