from flask import request, current_app, jsonify, Response, session
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required

from my_apps.utils.decorators import (
    x_api_key_required,
    user_not_exist,
)
from my_apps.utils.response import customResponse
from my_apps.users.models import (
    User,
    user_fields,
)
from my_apps import (
    APIView,
    db,
)


class DeleteUserView(APIView):
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
        {
            "in": "path",
            "name": "User ID",
            "required": True,
            "schema": {
                "type": "integer",
            }
        }
    ]
    responses = {
        200: {
            "description": "User deleted successful",
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

    @jwt_required()
    @x_api_key_required
    @user_not_exist
    @cross_origin(supports_credentials=True)
    def delete(self, user_id):
        user = self._get_user(user_id)
        if user is None:
            return customResponse({"message": 'User does not exist'}, status=404)

        db.session.delete(user)
        db.session.commit()

        return customResponse({"message": 'User deleted successful'}, status=200)

    def _get_user(self, user_id):
        return User.query.get(user_id)
