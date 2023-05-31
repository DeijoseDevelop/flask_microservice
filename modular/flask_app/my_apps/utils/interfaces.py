from flask_restful import Resource
from flasgger import SwaggerView


class APIView(Resource, SwaggerView):
    pass