from dataclasses import dataclass


@dataclass
class User(object):
    _email: str
    _password: str

    def get_email(self):
        return self._email

    def get_password(self):
        return self._password

    @classmethod
    def create_user_from_dict(cls, user: dict):
        cls(**user)
