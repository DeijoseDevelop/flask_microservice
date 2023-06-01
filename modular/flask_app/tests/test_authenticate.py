from base import BaseTest
from my_apps import app, db


class AuthenticateTest(BaseTest):

    def setUp(self):
        super(AuthenticateTest, self).setUp()

    def tearDown(self):
        super(AuthenticateTest, self).tearDown()

    def test_method_http_invalid(self):
        response = self.client.get(
            f'{self.TEST_URL}/api/v1/users/login/',
            data=self.to_json(self.fake_user),
            headers=self.headers,
        )

        self.assertEqual(response.reason, "METHOD NOT ALLOWED")
        self.assertEqual(response.status_code, 405)

    def test_not_x_api_key_in_authentication(self):
        self.headers.pop('x-api-key')
        response, status_code = self._login_test(self.fake_user)

        self.assertEqual(response['message'], "X-API-KEY header is required")
        self.assertEqual(status_code, 401)

    def test_x_api_key_invalid(self):
        self.headers['x-api-key'] = "lorem ipsum"
        response, status_code = self._login_test(self.fake_user)

        self.assertEqual(response['message'], "X-API-KEY invalid",)
        self.assertEqual(status_code, 401)

    def test_authenticate_email_invalid(self):
        response, status_code = self._login_test(self.fake_user)

        self.assertEqual(response['message'], "User does not exist")
        self.assertEqual(status_code, 404)

    def test_authenticate_password_invalid(self):
        self.fake_user['email'] = "user@example.com"
        response, status_code = self._login_test(self.fake_user)

        self.assertEqual(response['message'], "Invalid password")
        self.assertEqual(status_code, 404)

    def test_authenticate_success(self):
        response, status_code = self._login_test(self.valid_user)

        self.assertEqual(response['message'], "Login successful")
        self.assertEqual(status_code, 200)
        self.assertIn('token', response)

    def test_not_auth_token_in_logout(self):
        response = self.client.get(
            f"{self.TEST_URL}/api/v1/users/logout/", headers=self.headers)

        self.assertEqual(response.json()['msg'], 'Missing Authorization Header')
        self.assertEqual(response.status_code, 401)

    def test_auth_token_invalid_in_logout(self):
        self.headers['Authorization'] = "Bearer lorem ipsum"
        response = self.client.get(
            f"{self.TEST_URL}/api/v1/users/logout/", headers=self.headers)

        self.assertEqual(
            "Bad Authorization header. Expected 'Authorization: Bearer <JWT>'", response.json()['msg'])
        self.assertEqual(response.status_code, 422)

    def test_logout_successful(self):
        self.set_authorization_header()
        response = self.client.get(
            f"{self.TEST_URL}/api/v1/users/logout/", headers=self.headers)

        self.assertEqual(response.json()['message'], "Logout successful")
        self.assertEqual(response.status_code, 200)
