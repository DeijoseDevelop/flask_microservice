from base import BaseTest
from my_apps import app, db


class UpdateTest(BaseTest):

    def setUp(self):
        super(UpdateTest, self).setUp()

    def tearDown(self):
        super(UpdateTest, self).tearDown()

    def test_update_user_without_params(self):
        self.set_authorization_header()
        response, status_code = self.put_request(
            "/api/v1/users/update/",
            {},
            1,
        )

        self.assertEqual(response['message'], "Fields are required: name, email or password")
        self.assertEqual(status_code, 404)

    def test_update_user_not_exist(self):
        self.set_authorization_header()
        response, status_code = self.put_request(
            "/api/v1/users/update/",
            {"name": "user1", "email": "user1@example.com"},
            0,
        )

        self.assertEqual(response['message'], "User does not exist")
        self.assertEqual(status_code, 404)

    def test_update_user_successful(self):
        self.set_authorization_header()
        response, status_code = self.put_request(
            "/api/v1/users/update/",
            {"name": "user1", "email": "user1@example.com"},
            1,
        )

        self.assertEqual(response['message'], "User updated successful")
        self.assertEqual(status_code, 200)

