from flask import Flask, jsonify, request, abort, render_template

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
    return render_template('index.html')


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
    data = request.get_json()

    store = find_store(name)

    name = data.get('name', None)
    price = data.get('price', None)

    if name is None or price is None:
        abort(400)

    store['items'].append({
        'name': data['name'],
        'price': data['price']
    })

    store_updated = find_store(name)

    return jsonify({
        'success': True,
        'store': store_updated
    })


@app.route('/stores/<string:name>/items', methods=['GET'])
def get_items_in_store(name):

    store = find_store(name)
    print(store)

    if store is None:
        abort(404)
    else:
        return jsonify({
            'success': True,
            'name': store['name'],
            'items': store['items']
        })


@app.route('/ping')
def ping():
    return jsonify({'ping': 'pong'})


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'bad request'
    }), 400


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'resource not found'
    }), 404


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'internal server error'
    }), 500


app.run(port=5000)
