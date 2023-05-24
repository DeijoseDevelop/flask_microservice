class User(object):
    def __init__(self, email: str, password: str):
        self._email = email
        self._password = password

    def get_email(self):
        return self._email

    def get_password(self):
        return self._password

    @classmethod
    def create_user_from_dict(cls, user: dict):
        cls(**user)
