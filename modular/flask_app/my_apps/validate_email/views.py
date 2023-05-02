from flask import Blueprint, request, current_app, jsonify, Response
import json


validate_email_app = Blueprint('validate_email', __name__)

@validate_email_app.route('/validate_email/', methods=['GET'])
def validate_email():
    return Response(json.dumps({"message": 'email valid'}))
