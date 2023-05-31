import json
from flask import Response


def customResponse(data: dict, status: int):

    return Response(json.dumps(data), mimetype='application/json', status=status)

