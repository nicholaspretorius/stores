from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

stores = []


class Store(Resource):
    def get(self, name):
        for store in stores:
            if store['name'] == name:
                return store

        return {'store': None}, 404


class StoreList(Resource):
    def get(self):
        return {'stores': stores}

    def post(self):
        data = request.get_json()
        store = {'name': data['name']}
        stores.append(store)

        return store, 201


api.add_resource(Store, '/stores/<string:name>')
api.add_resource(StoreList, '/stores')

app.run(port=5000, debug=True)
