from flask import Flask
import secrets
from my_apps import app
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import timedelta


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
