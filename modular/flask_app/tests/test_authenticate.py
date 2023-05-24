from base import BaseTest

import os

from dotenv import load_dotenv


load_dotenv()


class AuthenticateTest(BaseTest):

    def setUp(self):
        self.fake_user = {
            "email": "example@gmail.com",
            "password": "example#password",
        }
        super(AuthenticateTest, self).setUp()

    def test_not_x_api_key_in_authentication(self):
        self.headers.pop('x-api-key')
        response = self.client.post(
            f'{self.TEST_URL}/api/v1/authenticate/',
            data=self.to_json(self.valid_user),
            headers=self.headers,
        )

        self.assertEqual(
            response.json()['message'], "X-API-KEY header is required")
        self.assertEqual(response.status_code, 401)

    def test_x_api_key_invalid(self):
        self.headers['x-api-key'] = "lorem ipsum"
        response = self.client.post(
            f'{self.TEST_URL}/api/v1/authenticate/',
            data=self.to_json(self.valid_user),
            headers=self.headers,
        )

        self.assertEqual(response.json()['message'], "X-API-KEY invalid",)
        self.assertEqual(response.status_code, 401)

    def test_authenticate_email_invalid(self):
        response = self.client.post(
            f'{self.TEST_URL}/api/v1/authenticate/',
            data=self.to_json(self.fake_user),
            headers=self.headers,
        )

        self.assertEqual(response.json()['message'], "Invalid email")
        self.assertEqual(response.status_code, 404)

    def test_authenticate_password_invalid(self):
        self.fake_user['email'] = os.getenv('AUTH_EMAIL')
        response = self.client.post(
            f'{self.TEST_URL}/api/v1/authenticate/',
            data=self.to_json(self.fake_user),
            headers=self.headers,
        )

        self.assertEqual(response.json()['message'], "Invalid password")
        self.assertEqual(response.status_code, 404)

    def test_authenticate_success(self):
        response, status_code = self.login_test()

        self.assertEqual(response['message'], "Login successful")
        self.assertEqual(status_code, 200)
        self.assertIn('token', response)

    def test_not_auth_token_in_logout(self):
        response = self.client.get(
            f"{self.TEST_URL}/api/v1/logout/", headers=self.headers)

        self.assertEqual(response.json()['msg'],
                         'Missing Authorization Header')
        self.assertEqual(response.status_code, 401)

    def test_auth_token_invalid_in_logout(self):
        self.headers['Authorization'] = "Bearer lorem ipsum"
        response = self.client.get(
            f"{self.TEST_URL}/api/v1/logout/", headers=self.headers)

        self.assertEqual(
            "Bad Authorization header. Expected 'Authorization: Bearer <JWT>'", response.json()['msg'])
        self.assertEqual(response.status_code, 422)

    def test_logout_successful(self):
        response, status_code = self.login_test()
        self.headers['Authorization'] = f"Bearer {response['token']}"
        response = self.client.get(
            f"{self.TEST_URL}/api/v1/logout/", headers=self.headers)

        self.assertEqual(response.json()['message'], "Logout successful")
        self.assertEqual(response.status_code, 200)
