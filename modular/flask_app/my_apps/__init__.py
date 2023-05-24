from flask import Flask
from flasgger import Swagger
from celery import Celery

import os


app = Flask(__name__)

# Swagger config
template = {
    "swagger": "2.0",
    "info": {
        "title": "Validate Email Microservice",
        "description": "API for validate email",
        "contact": {
            "responsibleOrganization": "Deiver Vazquez",
            "responsibleDeveloper": "Deiver Vazquez",
            "email": "dvazquez@lsv-tech.com",
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
from my_apps.authenticate.views import authenticate_app


# we record the views
app.register_blueprint(authenticate_app)
