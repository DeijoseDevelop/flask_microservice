from flask import Blueprint, request, current_app, jsonify, Response, session
from flask_cors import cross_origin
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
import json


login_app = Blueprint('login', __name__)


@login_app.route('/login/', methods=['POST'])
@cross_origin(supports_credentials=True)
def login_endpoint():
    data = request.json
    email = data['email']
    password = data['password']

    user = {
        "email": 'admin@lsv-tech.com',
        "password": 'admin1213'
    }

    if user['email'] != email:
        return Response(json.dumps({"message": 'Invalid email'}), mimetype='application/json', status=500)

    if user['password'] != password:
        return Response(json.dumps({"message": 'Invalid password'}), mimetype='application/json', status=500)

    access_token = create_access_token(identity=email)

    session['user'] = user
    session['token'] = access_token

    current_app.logger.debug(f'access_token: {access_token}')
    return Response(json.dumps({"message": 'Login successful', "token": access_token, "data": user}), mimetype='application/json', status=200)


@login_app.route('/logout/', methods=['POST'])
@jwt_required()
@cross_origin(supports_credentials=True)
def logout():
    session.pop('user', None)
    session.pop('token', None)
    current_app.logger.debug(f'session: {session}')
    return Response(json.dumps({"message": 'Logout successful'}), mimetype='application/json', status=200)
