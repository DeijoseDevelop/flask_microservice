from my_apps import app
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

import os
import secrets
from datetime import timedelta


## charge enviroment variables
load_dotenv()

# secret key for mongo session
tokens_session = secrets.token_hex(20)
app.config["SECRET_KEY"] = tokens_session

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = tokens_session
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=2)
jwt = JWTManager(app)

app.config['TIMEZONE'] = 'America/Bogota'


# user for authentication
app.config['user'] = {
    "email": os.getenv("AUTH_EMAIL"),
    "password": os.getenv("AUTH_PASSWORD"),
}

app.config['X-API-KEY'] = os.getenv("X_API_KEY")

class BaseConfig(object):
    'Base configuration'
    TESTING = False
    DEBUG = True
    #SECRET_KEY = tokens_session


class ProductionConfig(BaseConfig):
    'Production configuration'
    DEBUG = False


class DevelopmentConfig(BaseConfig):
    'Development configuration'
    TESTING = True
