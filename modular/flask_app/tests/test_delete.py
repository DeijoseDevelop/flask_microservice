from base import BaseTest
from my_apps import app, db


class DeleteTest(BaseTest):

    def setUp(self):
        super(DeleteTest, self).setUp()

    def tearDown(self):
        super(DeleteTest, self).tearDown()

    def test_delete_user_not_exist(self):
        self.set_authorization_header()
        response, status_code = self.delete_request(
            "/api/v1/users/delete/",
            0,
        )

        self.assertEqual(response['message'], "User does not exist")
        self.assertEqual(status_code, 404)

    def test_delete_user_successful(self):
        self.set_authorization_header()
        response, status_code = self.delete_request(
            "/api/v1/users/delete/",
            1,
        )

        self.assertEqual(response['message'], "User deleted successful")
        self.assertEqual(status_code, 200)

