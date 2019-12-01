from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

stores = []


class Store(Resource):
    def get(self, name):
        pass

    def post(self, name):
        pass


class StoreList(Resource):
    def get(self, name):
        pass


api.add_resource(Store, '/stores/<string:name>')
api.add_resource(StoreList, '/stores')

app.run(port=5000, debug=True)
