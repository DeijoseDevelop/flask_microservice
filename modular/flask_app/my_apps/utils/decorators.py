from flask import request, Response, current_app

import os
import json

from dotenv import load_dotenv


load_dotenv()


def x_api_key_required(method):
    def wrapper(*args, **kwargs):
        x_api_key = request.headers.get("X-Api-Key", False)

        if not x_api_key:
            return Response(json.dumps({"message": 'X-API-KEY header is required'}), mimetype='application/json', status=401)

        if x_api_key != os.getenv("X_API_KEY"):
            return Response(json.dumps({"message": 'X-API-KEY invalid'}), mimetype='application/json', status=401)

        return method(*args, **kwargs)

    return wrapper
