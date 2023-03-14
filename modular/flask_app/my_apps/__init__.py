from flask import Flask
from flask_login import LoginManager
from flask_odoo import Odoo
from celery import Celery

app = Flask(__name__)
UPLOAD_FOLDER = 'modular/flask_app/my_apps/static/uploads'
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

odoo = Odoo(app)

# ? celery config
app.config["CELERY_BROKER_URL"] = "redis://redis:6379"
celery = Celery(app.name, broker=app.config["CELERY_BROKER_URL"])
celery.conf.update(app.config)

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "login.login"

from my_apps.general.views import general
from my_apps.login.views import login

# we record the views
app.register_blueprint(general)
app.register_blueprint(login)
