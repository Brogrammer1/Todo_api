import os
import tempfile
import pytest

import app


from resources import todos
import models

@pytest.fixture
def client():
    """ this client setup was adapted from flask pocoo.org
    test cases seem to affect the database
    """
    db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
    app.app.config['TESTING'] = True
    client = app.app.test_client()

    yield client

    os.close(db_fd)
    os.unlink(app.app.config['DATABASE'])


def test_todo_or_404():
    todo = todos.todo_or_404(1)
    assert 'clean' in todo.name



def test_todo_list_get(client):
    res = client.get('/api/v1/todos')

    assert b'clean' in res.data
    assert res.status_code == 200


def test_todo_get(client):
    res = client.get('/api/v1/todos/1')
    assert b'clean the house' in res.data
    assert res.status_code == 200

def test_todo_get_fail(client):
    res = client.get('/api/v1/todos/100')
    assert res.status_code == 404


def test_todo_put(client):
    res = client.put('/api/v1/todos/7', json={'name': 'telly'})
    assert b'telly' in res.data
    assert res.status_code == 200


def test_todo_put_fail(client):
    res = client.put('/api/v1/todos/7', )
    assert b'Name of todo' in res.data
    assert res.status_code == 400


def test_todo_list_post(client):
    res = client.post('/api/v1/todos', json={'name': 'tell tell'},
                      headers={"Authorization": "Basic dGVzdDpwYXNzd29yZA=="})
    assert res.status_code == 201
    assert b'tell tell' in res.data


def test_todo_list_post_fail(client):
    res = client.post('/api/v1/todos',
                      headers={"Authorization": "Basic dGVzdDpwYXNzd29yZA=="})
    assert res.status_code == 400
    assert b'Name of todo' in res.data


def test_todo_delete(client):
    res = client.delete('/api/v1/todos/5', headers={
        "Authorization": "Basic dGVzdDpwYXNzd29yZA=="})
    assert res.status_code == 204
    assert b'' in res.data
