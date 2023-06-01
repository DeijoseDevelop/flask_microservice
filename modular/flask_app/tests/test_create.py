from base import BaseTest
from my_apps import app, db


class CreateTest(BaseTest):

    def setUp(self):
        super(CreateTest, self).setUp()

    def tearDown(self):
        super(CreateTest, self).tearDown()

    def test_create_user_without_params(self):
        response, status_code = self.post_request(
            "/api/v1/users/create/",
            {"name": "user", "email": "user@example.com"}
        )

        self.assertEqual(response['message'], "Fields are required: name, email or password")
        self.assertEqual(status_code, 404)

    def test_create_user_valid_params(self):
        response, status_code = self.post_request(
            "/api/v1/users/create/",
            {"name": "user", "email": "user2@example.com", "password": "password"}
        )

        self.assertEqual(response['message'], "User created succesful")
        self.assertEqual(status_code, 201)