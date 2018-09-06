from flask import Blueprint, abort
from flask_restful import (Resource, Api, reqparse,
                           fields, marshal,
                           marshal_with)

import models
from auth import basic_auth


def todo_or_404(todo_id):
    """gets model_todo or returns 404"""
    try:
        todo = models.Todo.get(models.Todo.id == todo_id)
    except models.Todo.DoesNotExist:
        abort(404)
    else:
        return todo


todo_fields = {
    'id': fields.Integer,
    'name': fields.String,
}


class TodoList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'name',
            required=True,
            help='Name of todo not provided',
            location=['form', 'json']
        )
        super().__init__()

    def get(self):
        """returns list of all Model_todos"""
        todos = [marshal(todo, todo_fields)
                 for todo in models.Todo.select()]
        return todos, 200

    @basic_auth.login_required
    @marshal_with(todo_fields)
    def post(self):
        """ creates model_todo and returns it """
        args = self.reqparse.parse_args()
        todo = models.Todo.create(**args)

        return todo, 201


class Todo(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'name',
            required=True,
            help='Name of todo not provided',
            location=['form', 'json']
        )
        super().__init__()

    @marshal_with(todo_fields)
    def get(self, id):
        """returns queried  model_todo"""
        return todo_or_404(id), 200

    @marshal_with(todo_fields)
    def put(self, id):
        """ updates a model_todo then returns it """
        args = self.reqparse.parse_args()
        query = models.Todo.update(**args).where(models.Todo.id == id)
        query.execute()
        return models.Todo.get(models.Todo.id == id), 200

    @basic_auth.login_required
    @marshal_with(todo_fields)
    def delete(self, id):
        """deletes a model_todo and returns an empty string """
        query = models.Todo.delete().where(models.Todo.id == id)
        query.execute()
        return '', 204


todos_api = Blueprint('resources.todos', __name__)
api = Api(todos_api)
api.add_resource(
    TodoList,
    '/api/v1/todos',
    endpoint='todos')

api.add_resource(
    Todo,
    '/api/v1/todos/<int:id>',
    endpoint='todo')
