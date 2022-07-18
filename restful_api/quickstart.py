# A MINIMAL API

from random import randint
from flask import Flask, url_for
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app=app)

class HelloWorld(Resource):
    def get(self):
        return {"hello":"world"}

api.add_resource(HelloWorld, '/')



# RESOURCEFUL ROUTING
from flask import Flask, request, redirect
from flask_restful import Resource, Api

app2 = Flask(__name__)
api2 = Api(app=app2)

todos = {"1": "something", "2": "something new"}

class TodoSimple(Resource):
    def get(self, todo_id):
        return {todo_id: todos[todo_id]}

    def put(self, todo_id):
        todos[todo_id] = request.form['data']
        return {todo_id: todos[todo_id]}, 201, {'Etag': 'some-opaque-string'}  # BODY, RESPONSE-CODE, HEADER

    def post(self, todo_id):
        todo_id = randint(0, 15)
        while todo_id in todos.keys():
            todo_id = randint(0, 15)
        todos[todo_id] = request.form['data']

        return self.get(todo_id=todo_id)

class RedirectEndpoint(Resource):
    def get(self):
        return redirect(location=url_for('todo_endpoint', todo_id="2"))

api2.add_resource(TodoSimple, '/<string:todo_id>', endpoint='todo_endpoint')
api2.add_resource(RedirectEndpoint, '/endpoint', endpoint='redirect_endpoint')



# DATA FORMATTING
from flask_restful import fields, marshal_with

resource_fields = {
    'todo_idd': fields.Integer,
    'task': fields.String,
    'uri': fields.Url('todo_dao_endpoint')
}

class TodoDAO:
    def __init__(self, id, task):
        self.todo_idd = id + 5 
        self.task = task
        self.status = 'Active'  # THIS FIELD WON'T BE SENT IN THE RESPONSE

class Todo(Resource):
    @marshal_with(resource_fields)
    def get(self, todo_id):
        return TodoDAO(id=todo_id, task="Remember the Vleague")
# TODO: werkzeug.routing.BuildError: Could not build url for endpoint 'todo_dao_endpoint' with values 
# ['status', 'task', 'todo_idd']. Did you forget to specify values ['todo_id']?
api2.add_resource(Todo, '/todo-dao/<int:todo_id>', endpoint='todo_dao_endpoint')

if __name__ == '__main__':
    app2.run(debug=True)