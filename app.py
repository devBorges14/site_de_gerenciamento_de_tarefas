"""
Crie uma aplicação web simples onde os usuários possam gerenciar suas tarefas diárias. 
O sistema permitirá adicionar, visualizar, atualizar e excluir tarefas. Além disso, 
inclua a funcionalidade de marcar uma tarefa como concluída.
"""

from flask import Flask, g, redirect, request, render_template
import sqlite3

app = Flask(__name__)

# Função para inicializar o banco de dados
def init_db():
    with sqlite3.connect('tasks.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY, 
                task TEXT,
                risk INTEGER DEFAULT 0
            )
        ''')
        conn.commit()

def get_db():
    """Conectar ao banco de dados e garantir que a conexão seja reutilizada durante a requisição"""
    if not hasattr(g, 'db'):
        g.db = sqlite3.connect('tasks.db')
        g.db.row_factory = sqlite3.Row  # Isso permite acessar as colunas como dicionários
    return g.db

@app.teardown_appcontext
def close_db(error):
    """Fechar a conexão com o banco de dados após a requisição"""
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

# Rota para exibir a lista de tarefas
@app.route('/')
def index():
    db = get_db()  # Conectar ao banco de dados
    cursor = db.cursor()
    cursor.execute('SELECT id, task, risk FROM tasks WHERE risk = 0')  # Exibe apenas as tarefas não concluídas
    tasks = cursor.fetchall()
    return render_template('index.html', tasks=tasks)


@app.route('/add', methods=['POST'])
def add_task():
    task = request.form.get('task')
    if task:
        db = get_db()  # Conectar ao banco de dados
        cursor = db.cursor()
        cursor.execute('INSERT INTO tasks (task) VALUES (?)', (task,))
        db.commit()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete_task(id):
    db = get_db()  # Conectar ao banco de dados
    cursor = db.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ?', (id,))
    db.commit()
    return redirect('/')

@app.route('/delete_all', methods=['POST'])
def delete_all_tasks():
    db = get_db()  # Conectar ao banco de dados
    cursor = db.cursor()
    cursor.execute('DELETE FROM tasks')  # Deletar todas as tarefas
    db.commit()
    return redirect('/')

@app.route('/completed')
def completed_tasks():
    db = get_db()  # Conectar ao banco de dados
    cursor = db.cursor()
    cursor.execute('SELECT id, task FROM tasks WHERE risk = 1')
    completed_tasks = cursor.fetchall()  # Recuperar todas as tarefas concluídas
    return render_template('completed_tasks.html', tasks=completed_tasks)

@app.route('/risk/<int:id>', methods=['GET'])
def mark_completed(id):
    db = get_db()  # Conectar ao banco de dados
    cursor = db.cursor()
    cursor.execute('UPDATE tasks SET risk = 1 WHERE id = ?', (id,))
    db.commit()
    return redirect('/')  # Redireciona para a página inicial

if __name__ == '__main__':
    init_db()  # Chama a função para garantir que a tabela seja criada
    app.run(debug=True, port=8000)
