import json

from flask import Blueprint, request, current_app, jsonify, Response, session
from flask_cors import cross_origin
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
)
from flask_restful import Api

from my_apps.utils.decorators import x_api_key_required
from my_apps.init_db import (
    User,
    user_fields,
)
from my_apps import (
    APIView,
    db,
)


users_app = Blueprint('users', __name__)
api = Api(users_app)

class CreateUserView(APIView):

    @x_api_key_required
    @cross_origin(supports_credentials=True)
    def post(self):
        data = request.json

        if data.get('name', False) or data.get('email', False) or data.get('password', False):
            Response(json.dumps({"message": 'fields are required: name, email and password'}), mimetype='application/json', status=404)

        user = User(
            name=data['name'],
            email=data['email'],
            password=data['password'],
        )

        current_app.logger.debug(f"USER: {user}")

        current_app.logger.debug(db.session.execute(db.select(User)).all())

        db.session.add(user)
        db.session.commit()

        return Response(json.dumps({"message": 'user created succesfully'}), mimetype='application/json', status=201)


class LoginUserView(APIView):

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

class LogoutUserView(APIView):

    @jwt_required()
    @x_api_key_required
    @cross_origin(supports_credentials=True)
    def get(self):
        session.pop('user', None)
        session.pop('token', None)
        return Response(json.dumps({"message": 'Logout successful'}), mimetype='application/json', status=200)


create_users_view = CreateUserView.as_view('create_users_view')
login_users_view = LoginUserView.as_view('login_users_view')
logout_users_view = LogoutUserView.as_view('logout_users_view')

# adding routes
users_app.add_url_rule(
    '/api/v1/users/create/',
    view_func=create_users_view, methods=['POST'],
)
users_app.add_url_rule(
    '/api/v1/users/login/',
    view_func=login_users_view, methods=['POST'],
)
users_app.add_url_rule(
    '/api/v1/users/logout/',
    view_func=logout_users_view, methods=['GET'],
)
