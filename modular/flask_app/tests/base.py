import os
import json
from abc import ABC, abstractmethod
from unittest import TestCase

import requests
from passlib.hash import bcrypt
from dotenv import load_dotenv

from my_apps import app, db
from my_apps.users.models import User


load_dotenv()

class BaseTest(TestCase, ABC):

    @abstractmethod
    def setUp(self):
        app.testing = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

        self.TEST_URL = os.getenv("TEST_URL")
        self.client = requests
        self.headers = {
            "Content-Type": 'application/json',
            'x-api-key': os.getenv("X_API_KEY")
        }

        self.valid_user = None
        with app.app_context():
            db.create_all()
        self._create_example_user()
        self.fake_user = {
            "name": "fakeuser",
            "email": "user@example2.com",
            "password": "user1",
        }

    @abstractmethod
    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def _create_example_user(self):
        user = {"name": "user", "email": "user@example.com", "password": "password"}
        response, status_code = self.post_request(
            "/api/v1/users/create/",
            user
        )
        user.pop("name")
        self.valid_user = user

    def set_authorization_header(self):
        token = self.get_token()

        self.headers['Authorization'] = f"Bearer {token}"

    def get_token(self):
        response, status_code = self._login_test(self.valid_user)
        return response['token']

    def _login_test(self, data):
        return self.post_request('/api/v1/users/login/', data)

    def post_request(self, url: str, data: dict):
        response = self.client.post(
            f'{self.TEST_URL}{url}',
            data=self.to_json(data),
            headers=self.headers,
        )

        return response.json(), response.status_code

    def put_request(self, url: str, data: dict, user_id: int):
        response = self.client.put(
            f'{self.TEST_URL}{url}{user_id}',
            data=self.to_json(data),
            headers=self.headers,
        )

        return response.json(), response.status_code

    def delete_request(self, url: str, user_id: int):
        response = self.client.delete(
            f'{self.TEST_URL}{url}{user_id}',
            headers=self.headers,
        )

        return response.json(), response.status_code

    def to_json(self, data: dict):
        return json.dumps(data)

