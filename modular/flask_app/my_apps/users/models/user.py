from flask_restful import fields
from my_apps import db, app


user_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "email": fields.String,
    "password": fields.String,
}

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'password': self.password,
        }

