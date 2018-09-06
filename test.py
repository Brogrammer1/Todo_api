import unittest

import app


class TestFlaskApi(unittest.TestCase):
    def setUp(self):
        self.app = app.app.test_client()

    def test_home_view(self):
        res = self.app.get('/')
        assert res.status_code == 200

    def test_todo_list_get(self):
        res = self.app.get('/api/v1/todos')

        assert b'clean' in res.data
        assert res.status_code == 200

    def test_todo_get(self):
        res = self.app.get('/api/v1/todos/1')
        assert b'clean the house' in res.data
        assert res.status_code == 200

    def test_todo_get_fail(self):
        res = self.app.get('/api/v1/todos/100')
        assert res.status_code == 404

    def test_todo_put(self):
        res = self.app.put('/api/v1/todos/7', json={'name': 'telly'})
        assert b'telly' in res.data
        assert res.status_code == 200

    def test_todo_put_fail(self):
        res = self.app.put('/api/v1/todos/7', )
        assert b'Name of todo' in res.data
        assert res.status_code == 400

    def test_todo_list_post(self):
        res = self.app.post('/api/v1/todos', json={'name': 'tell tell'},
                            headers={
                                "Authorization": "Basic dGVzdDpwYXNzd29yZA=="})
        assert res.status_code == 201
        assert b'tell tell' in res.data

    def test_todo_list_post_fail(self):
        res = self.app.post('/api/v1/todos',
                            headers={
                                "Authorization": "Basic dGVzdDpwYXNzd29yZA=="})
        assert res.status_code == 400
        assert b'Name of todo' in res.data

    def test_todo_delete(self):
        res = self.app.delete('/api/v1/todos/5', headers={
            "Authorization": "Basic dGVzdDpwYXNzd29yZA=="})
        assert res.status_code == 204
        assert b'' in res.data


if __name__ == "__main__":
    unittest.main()
