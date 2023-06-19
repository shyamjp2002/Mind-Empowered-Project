from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def __init__(self, task, completed=False):
        self.task = task
        self.completed = completed
with app.app_context():     
    db.create_all()

@app.route('/todos', methods=['GET'])
def get_todos():
    todos = Todo.query.all()
    output = []
    for todo in todos:
        todo_data = {'id': todo.id, 'task': todo.task, 'completed': todo.completed}
        output.append(todo_data)
    return jsonify(output)

@app.route('/todos', methods=['POST'])
def add_todo():
    data = request.get_json()
    new_todo = Todo(task=data['task'])
    db.session.add(new_todo)
    db.session.commit()
    return jsonify({'message': 'Todo created successfully!'})

@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if not todo:
        return jsonify({'message': 'Todo not found!'})
    data = request.get_json()
    todo.task = data['task']
    todo.completed = data['completed']
    db.session.commit()
    return jsonify({'message': 'Todo updated successfully!'})

@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if not todo:
        return jsonify({'message': 'Todo not found!'})
    db.session.delete(todo)
    db.session.commit()
    return jsonify({'message': 'Todo deleted successfully!'})

if __name__ == '__main__':
    app.run(debug=True)
