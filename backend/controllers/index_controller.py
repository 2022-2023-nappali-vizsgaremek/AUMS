from flask_restful import Resource
from flask_apispec.views import MethodResource

class Index(MethodResource, Resource):
    def get(self):
        return {'message': 'AUMS'}, 200