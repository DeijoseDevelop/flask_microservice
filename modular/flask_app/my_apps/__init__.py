import os

from flask import Flask
from flasgger import Swagger
from celery import Celery
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_rest_paginate import Pagination
from dotenv import load_dotenv

from my_apps.utils.interfaces import *


load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@db:5432/{os.getenv('POSTGRES_DB')}"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Possible configurations for Paginate
app.config['PAGINATE_PAGE_SIZE'] = 10
app.config['PAGINATE_DATA_OBJECT_KEY'] = "results"
pagination = Pagination(app, db)

# Swagger config
template = {
    "swagger": "2.0",
    "info": {
        "title": "Users management microservice",
        "description": "Microservice created by me",
        "contact": {
            "responsibleOrganization": "LSV",
            "responsibleDeveloper": "LSV Developer",
            "email": "lsvdeveloper@lsv-tech.com",
        },
        "version": "0.1.0"
    },
}

swagger = Swagger(app, template=template)

app.config["UPLOAD_FOLDER"] = os.getenv("UPLOAD_FOLDER")

# ? celery config
app.config["CELERY_BROKER_URL"] = "redis://redis:6379"
celery = Celery(app.name, broker=app.config["CELERY_BROKER_URL"])
celery.conf.update(app.config)

# apps
from my_apps.users.views import users_app


# we record the views
app.register_blueprint(users_app)
