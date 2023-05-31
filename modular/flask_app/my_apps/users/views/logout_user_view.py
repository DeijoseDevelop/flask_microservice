from flask import request, current_app, Response, session
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required

from my_apps.utils.decorators import x_api_key_required
from my_apps.utils.response import customResponse
from my_apps import (
    APIView,
)


class LogoutUserView(APIView):
    parameters = [
        {
            'in': 'header',
            'name': 'x-api-key',
            'type': 'string',
            'required': True,
            'description': 'API key for authentication'
        },
        {
            'in': 'header',
            'name': 'Authorization',
            'type': 'string',
            'required': True,
            'description': 'Access token for authentication'
        },
    ]
    responses = {
        200: {
            "description": "Logout successful",
            "schema": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "Success message"
                    },
                }
            }
        },
    }

    @jwt_required()
    @x_api_key_required
    @cross_origin(supports_credentials=True)
    def get(self):
        session.pop('token', None)
        return customResponse({"message": 'Logout successful'}, status=200)

