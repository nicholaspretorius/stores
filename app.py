from flask import Flask, jsonify, request

app = Flask(__name__)

stores = [
    {
        'name': 'Wakemaps',
        'items': [
            {
                'name': 'Liquid Force TAO Wakeskate',
                'price': 5999.99
            }
        ]
    }
]


@app.route('/')
def home():
    return jsonify({'hello': 'world'})


@app.route('/stores', methods=['GET'])
def get_stores():
    return jsonify({'stores': stores})


@app.route('/stores', methods=['POST'])
def create_store():
    body = request.get_json()
    name = body.get('name', None)

    stores.append({'name': name, 'items': []})

    return jsonify({
        'success': True,
        'store': name,
        'stores': stores
    })


@app.route('/stores/<string:name>', methods=['GET'])
def get_store(name):

    store = stores[name]

    return jsonify({
        'success': True,
        'store': store
    })


@app.route('/stores/<string:name>/items', methods=['POST'])
def create_item_in_store(name):
    body = request.get_json()
    name = body.get('name', None)
    price = int(request.get('price', None))

    stores[name].items.append({'name': name, 'price': price})

    return jsonify({
        'success': True,
        'store': stores[name]
    })


@app.route('/stores/<string:name>/items', methods=['GET'])
def get_items_in_store(name):

    return jsonify({
        'success': True,
        'store': stores[name]
    })


@app.route('/ping')
def ping():
    return jsonify({'ping': 'pong'})


app.run(port=5000)
