from flask import Blueprint, request, current_app, jsonify, Response, session
from flask_cors import cross_origin
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
)
from flasgger import SwaggerView

import json

from my_apps.utils.decorators import x_api_key_required


authenticate_app = Blueprint('authenticate', __name__)

class AuthenticateView(SwaggerView):
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
            "description": "Invalid email or password",
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
        email = data['email']
        password = data['password']

        user = current_app.config['user']

        if user['email'] != email:
            return Response(json.dumps({"message": 'Invalid email'}), mimetype='application/json', status=404)

        if user['password'] != password:
            return Response(json.dumps({"message": 'Invalid password'}), mimetype='application/json', status=404)

        access_token = create_access_token(identity=email)

        session['user'] = user
        session['token'] = access_token

        return Response(json.dumps({"message": 'Login successful', "token": access_token}), mimetype='application/json', status=200)


class LogoutView(SwaggerView):
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
        }
    ]
    responses = {
        200: {
            "description": "Logout successful",
        },
    }

    @jwt_required()
    @x_api_key_required
    @cross_origin(supports_credentials=True)
    def get(self):
        session.pop('user', None)
        session.pop('token', None)
        return Response(json.dumps({"message": 'Logout successful'}), mimetype='application/json', status=200)


authenticate_view = AuthenticateView.as_view('authenticate_view')
logoutView = LogoutView.as_view('logout_view')

# adding routes
authenticate_app.add_url_rule(
    '/api/v1/authenticate/',
    view_func=authenticate_view,
    methods=['POST'],
)
authenticate_app.add_url_rule(
    '/api/v1/logout/',
    view_func=logoutView,
    methods=['GET'],
)
