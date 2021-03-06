import datetime

from argon2 import PasswordHasher
from peewee import *

DATABASE = SqliteDatabase('todos.sqlite')
HASHER = PasswordHasher()


class Todo(Model):
    name = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE


class User(Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()

    class Meta:
        database = DATABASE

    @classmethod
    def create_user(cls, username, email, password):
        email = email.lower()
        try:
            cls.select().where(
                (cls.email == email) | (cls.username ** username)
            ).get()
        except cls.DoesNotExist:
            user = cls(username=username, email=email)
            user.password = user.set_password(password)
            user.save()
            return user
        else:
            raise Exception("User with that email or username already exists")

    @staticmethod
    def set_password(password):
        return HASHER.hash(password)

    def verify_password(self, password):
        return HASHER.verify(self.password, password)


def create_test_user():
    try:
        User.get(User.username == 'test')

    except User.DoesNotExist:
        User.create_user('test', 'test@example.com', 'password')


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Todo], safe=True)
    DATABASE.close()
