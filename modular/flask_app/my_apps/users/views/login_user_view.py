from passlib.hash import bcrypt
from flask import request, current_app, jsonify, Response, session
from flask_cors import cross_origin
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
)

from my_apps.utils.decorators import x_api_key_required
from my_apps.utils.response import customResponse
from my_apps.users.models import (
    User,
    user_fields,
)
from my_apps import (
    APIView,
    db,
)


class LoginUserView(APIView):
    parameters = [
        {
            'in': 'header',
            'name': 'x-api-key',
            'type': 'string',
            'required': True,
            'description': 'API key for authentication'
        },
        {
            "in": "body",
            "name": "credentials",
            "description": "User credentials",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "email": {
                        "type": "string",
                        "example": "user@example.com"
                    },
                    "password": {
                        "type": "string",
                        "example": "mypassword"
                    }
                }
            }
        }
    ]
    responses = {
        200: {
            "description": "Login successful",
            "schema": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "Success message"
                    },
                    "token": {
                        "type": "string",
                        "description": "Access token"
                    }
                }
            }
        },
        404: {
            "description": "User does not exist",
            "schema": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "Error message"
                    }
                }
            }
        }
    }

    @x_api_key_required
    @cross_origin(supports_credentials=True)
    def post(self):
        data = request.json

        if not data.get('email', False) or not data.get('password', False):
            return customResponse({"message": 'fields are required: email and password'}, status=404)

        email = data['email']
        password = data['password']

        query = self._get_user(email)

        if len(query) == 0:
            return customResponse({"message": 'User does not exist'}, status=404)

        user = query[0][0]

        if not bcrypt.verify(password, user.password):
            return customResponse({"message": 'Invalid password'}, status=404)

        access_token = self._create_token(email)

        return customResponse({"message": 'Login successful', "token": access_token}, status=200)

    def _get_user(self, email: str):
        return db.session.execute(db.select(User).filter_by(email=email)).fetchall()

    def _create_token(self, email: str):
        access_token = create_access_token(identity=email)
        session['token'] = access_token
        return access_token

