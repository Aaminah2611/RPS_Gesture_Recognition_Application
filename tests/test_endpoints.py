import os
import unittest
import json
from backend.app import app


class TestEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        os.chdir('../backend/')

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_start_game(self):
        response = self.app.post('/start')
        self.assertEqual(response.status_code, 302)  # Redirect status code

    def test_reset_game(self):
        response = self.app.post('/reset')
        self.assertEqual(response.status_code, 302)  # Redirect status code

    def test_quit_game(self):
        response = self.app.post('/quit')
        self.assertEqual(response.status_code, 302)  # Redirect status code

    # def test_create_user(self):
    #     data = {'username': 'test_user', 'password': 'test_password'}
    #     response = self.app.post('/create_user', data=data)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(json_data['message'], 'User created successfully')

    def test_create_game(self):
        data = {'user_id': 1}  # Provide a valid user_id for testing
        response = self.app.post('/create_game', data=data)
        # self.assertEqual(data_data['message'], 'Game created successfully')

    # Add more test cases for other endpoints...


if __name__ == '__main__':
    unittest.main()
