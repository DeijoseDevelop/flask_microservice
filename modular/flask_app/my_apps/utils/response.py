import json

from flask import Response


class CustomResponse(Response):
    def __init__(self, response=None, status=None, headers=None, mimetype=None):
        if isinstance(response, (dict, list)):
            response = json.dumps(response)

        if mimetype is None:
            mimetype = "application/json"

        super().__init__(response, status, headers, mimetype)

