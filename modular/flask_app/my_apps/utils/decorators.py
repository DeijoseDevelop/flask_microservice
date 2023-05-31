import json
import os

from flask import request, Response, current_app
from sqlalchemy.exc import (
    IntegrityError,
    NoResultFound,
)
from dotenv import load_dotenv


load_dotenv()

def user_not_exist(method):
    def wrapper(*args, **kwargs):
        try:
            return method(*args, **kwargs)
        except NoResultFound as error:
            return Response(json.dumps({"message": "User does not exist"}), mimetype='application/json', status=500)

    return wrapper

def check_unique_email(method):
    def wrapper(*args, **kwargs):
        try:
            return method(*args, **kwargs)
        except IntegrityError as error:
            return Response(json.dumps({"message": "The email address is already registered"}), mimetype='application/json', status=500)

    return wrapper

def x_api_key_required(method):
    def wrapper(*args, **kwargs):
        x_api_key = request.headers.get("X-Api-Key", False)

        if not x_api_key:
            return Response(json.dumps({"message": 'X-API-KEY header is required'}), mimetype='application/json', status=401)

        if x_api_key != os.getenv("X_API_KEY"):
            return Response(json.dumps({"message": 'X-API-KEY invalid'}), mimetype='application/json', status=401)

        return method(*args, **kwargs)

    return wrapper
