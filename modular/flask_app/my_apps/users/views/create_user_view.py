from passlib.hash import bcrypt
from flask import request, current_app, jsonify, Response, session
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required

from my_apps.utils.decorators import (
    x_api_key_required,
    check_unique_email,
)
from my_apps.utils.response import customResponse
from my_apps.users.models import User

from my_apps import (
    APIView,
    db,
    app,
)

class CreateUserView(APIView):

    parameters =[
        {
            'in': 'header',
            'name': 'x-api-key',
            'type': 'string',
            'required': True,
            'description': 'API key for authentication'
        },
        {
            "in": "body",
            "name": "name",
            "description": "User name",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "example": "Jhon Doe"
                    },
                }
            }
        },
        {
            "in": "body",
            "name": "email",
            "description": "User email",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "email": {
                        "type": "string",
                        "example": "user@example.com"
                    },
                }
            }
        },
        {
            "in": "body",
            "name": "password",
            "description": "User password",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "password": {
                        "type": "string",
                        "example": "jhondoe123"
                    },
                }
            }
        },
    ]
    responses = {
        201: {
            "description": "User created",
            "schema": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "User created succesful",
                    }
                }
            }
        },
        404: {
            "description": "Fields required",
            "schema": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "Fields are required: name, email and password",
                    }
                }
            }
        },
    }


    @x_api_key_required
    @check_unique_email
    @cross_origin(supports_credentials=True)
    def post(self):
        data = request.json

        if not data.get('name', False) or not data.get('email', False) or not data.get('password', False):
            return customResponse({"message": 'Fields are required: name, email or password'}, status=404)

        user = User(
            name=data['name'],
            email=data['email'],
            password=bcrypt.hash(data['password']),
        )

        self._create_table()
        self._insert_user(user)

        return customResponse({"message": 'User created succesful'}, status=201)

    def _create_table(self):
        with app.app_context():
            db.create_all()

    def _insert_user(self, user):
        db.session.add(user)
        db.session.commit()

