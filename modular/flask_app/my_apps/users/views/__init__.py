import json

from flask import Blueprint
from flask_restful import Api

from my_apps.users.views.create_user_view import CreateUserView
from my_apps.users.views.login_user_view import LoginUserView
from my_apps.users.views.logout_user_view import LogoutUserView
from my_apps.users.views.list_user_view import ListUserView
from my_apps.users.views.delete_user_view import DeleteUserView
from my_apps.users.views.update_user_view import UpdateUserView


users_app = Blueprint('users', __name__)
api = Api(users_app)

# adding routes
create_users_view = CreateUserView.as_view('create_users_view')
login_users_view = LoginUserView.as_view('login_users_view')
logout_users_view = LogoutUserView.as_view('logout_users_view')
list_users_view = ListUserView.as_view('list_users_view')
delete_users_view = DeleteUserView.as_view('delete_users_view')
update_users_view = UpdateUserView.as_view('update_users_view')


users_app.add_url_rule(
    '/api/v1/users/create/',
    view_func=create_users_view, methods=['POST'],
)
users_app.add_url_rule(
    '/api/v1/users/login/',
    view_func=login_users_view, methods=['POST'],
)
users_app.add_url_rule(
    '/api/v1/users/logout/',
    view_func=logout_users_view, methods=['GET'],
)
users_app.add_url_rule(
    '/api/v1/users/list/',
    view_func=list_users_view, methods=['GET'],
)
users_app.add_url_rule(
    '/api/v1/users/delete/<int:user_id>',
    view_func=delete_users_view, methods=['DELETE'],
)
users_app.add_url_rule(
    '/api/v1/users/update/<int:user_id>',
    view_func=update_users_view, methods=['PUT'],
)