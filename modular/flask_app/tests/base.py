from my_apps import app

from abc import ABC, abstractmethod
from unittest import TestCase
import os
import json

import requests


class BaseTest(TestCase, ABC):

    @abstractmethod
    def setUp(self):
        app.testing = True
        self.TEST_URL = os.getenv("TEST_URL")
        self.client = requests
        self.headers = {
            "Content-Type": 'application/json',
            'x-api-key': os.getenv("X_API_KEY")
        }
        self.valid_user = {
            "email": os.getenv("AUTH_EMAIL"),
            "password": os.getenv("AUTH_PASSWORD"),
        }

    def to_json(self, data: dict):
        return json.dumps(data)

    def login_test(self):
        response = self.client.post(
            f'{self.TEST_URL}/api/v1/authenticate/',
            data=json.dumps(self.valid_user),
            headers=self.headers,
        )

        return response.json(), response.status_code
