from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

stores = []


class Store(Resource):
    def get(self, name):
        store = next(filter(lambda x: x['name'] == name, stores), None)

        return {'store': store}, 200 if store else 404

        # for store in stores:
        #     if store['name'] == name:
        #         return store

        # return {'store': None}, 404

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, stores), None):
            return {'message': "A store with name '{}' already exists. ".format(name)}, 400
        else:
            data = request.get_json()
            store = {'name': data['name']}
            stores.append(store)

            return store, 201


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
