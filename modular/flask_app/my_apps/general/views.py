from flask import Blueprint, request, current_app, jsonify, Response
from flask_cors import cross_origin
import os
import json


general_app = Blueprint('general', __name__)


@general_app.route('/general/', methods=['GET'])
# @cross_origin(supports_credentials=True)
def general():
    data = {
        "message": 'Hello world!!!'
    }
    return Response(json.dumps(data), mimetype='application/json', status=200)
