from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime

app = Flask(__name__)

tasks = []
deleted_count = 0

@app.route('/')
def index():
    total = len(tasks)
    completed = sum(1 for t in tasks if t['done'])
    remaining = total - completed
    return render_template('index.html', tasks=tasks, total=total,
                           completed=completed, remaining=remaining,
                           deleted=deleted_count)

@app.route('/add', methods=['POST'])
def add():
    task = request.form.get('task')
    due_date = request.form.get('due_date')
    due_time = request.form.get('due_time')
    if task:
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tasks.append({
            'name': task,
            'done': False,
            'created_at': created_at,
            'due_date': due_date,
            'due_time': due_time
        })
    return redirect(url_for('index'))

@app.route('/toggle/<int:task_id>', methods=['POST'])
def toggle(task_id):
    if 0 <= task_id < len(tasks):
        tasks[task_id]['done'] = not tasks[task_id]['done']
    total = len(tasks)
    completed = sum(1 for t in tasks if t['done'])
    remaining = total - completed
    return jsonify({'completed': completed, 'remaining': remaining})

@app.route('/delete/<int:task_id>')
def delete(task_id):
    global deleted_count
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
        deleted_count += 1
    return redirect(url_for('index'))

@app.route('/reset')
def reset():
    global tasks, deleted_count
    tasks = []
    deleted_count = 0
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
