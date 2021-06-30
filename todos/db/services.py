from uuid import uuid4
from pynamodb.exceptions import DoesNotExist
from todos.serializers import TodoCreateSerializer, TodoSerializer
from todos.db.models import TodoModel


class TodosDBService:
    def get_todos(self):
        todos = TodoModel.scan()
        return [todo.serialized for todo in todos]

    def get_todo(self, id: str):
        try:
            todo = TodoModel.get(id)
        except DoesNotExist:
            return None
        else:
            return todo.serialized

    def create_todo(self, todo_serializer: TodoCreateSerializer):
        todo = TodoModel(
            str(uuid4()),
            **todo_serializer.dict()
        )
        todo.save()
        return todo.serialized

    def update_todo(self, todo_serializer: TodoSerializer):
        try:
            todo_model = TodoModel.get(todo_serializer.id)
        except DoesNotExist:
            return None
        else:
            todo_model.title = todo_serializer.title
            todo_model.save()
            return todo_model.serialized

    def delete_todo(self, id: str):
        try:
            todo = TodoModel.get(id)
        except DoesNotExist:
            return False
        else:
            todo.delete()
            return True