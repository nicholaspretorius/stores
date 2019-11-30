from flask import Flask, jsonify, request, abort

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
    },
    {
        'name': 'Stoke City Wakepark',
        'items': []
    }
]


@app.route('/')
def home():
    return jsonify({
        'success': True,
        'hello': 'world'
    })


@app.route('/stores', methods=['GET'])
def get_stores():
    return jsonify({
        'success': True,
        'stores': stores
    })


@app.route('/stores', methods=['POST'])
def create_store():
    data = request.get_json()
    new_store = {
        'name': data['name'],
        'items': []
    }

    stores.append(new_store)

    return jsonify({
        'success': True,
        'store': new_store
    })


def format_name(name):
    return name.replace(' ', '-').lower()


def find_store(name):
    found = None
    for store in stores:
        store_name = format_name(store['name'])
        url_name = format_name(name)
        print(store_name, ': ', url_name)
        if store_name == url_name:
            found = store

    return found


@app.route('/stores/<string:name>', methods=['GET'])
def get_store(name):

    store = find_store(name)

    if store is None:
        abort(404)
    else:
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
    pass


@app.route('/ping')
def ping():
    return jsonify({'ping': 'pong'})


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'resource not found'
    }), 404


app.run(port=5000)
