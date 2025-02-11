from flask import Flask, jsonify, request
from flask_cors import CORS
import uuid

app = Flask(__name__)

app.config.from_object(__name__)

# Allow all origins (for development)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# OR allow only your Vue frontend (more secure)
CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}},
     allow_headers=["Content-Type", "Authorization"],
     supports_credentials=True)

@app.route('/', methods=['GET'])
def greetings():
    return("This is the library API.")

ITEMS = [
    {'id': uuid.uuid4().hex, 'title': 'War and Peace', 'genre': 'Historical', 'available': False},
    {'id': uuid.uuid4().hex, 'title': 'Crime and Punishment', 'genre': 'Psychological', 'available': True},
    {'id': uuid.uuid4().hex, 'title': 'The Book Thief', 'genre': 'Historical Fiction', 'available': True},
    {'id': uuid.uuid4().hex, 'title': 'Dune', 'genre': 'Science Fiction', 'available': False},
    {'id': uuid.uuid4().hex, 'title': 'The Hitchhiker\'s Guide to the Galaxy', 'genre': 'Science Fiction', 'available': True},
    {'id': uuid.uuid4().hex, 'title': 'The Shining', 'genre': 'Horror', 'available': False},
    {'id': uuid.uuid4().hex, 'title': 'Dracula', 'genre': 'Horror', 'available': True},
    {'id': uuid.uuid4().hex, 'title': 'The Road', 'genre': 'Post-Apocalyptic', 'available': True}
]

@app.route('/items', methods=['GET', 'POST'])
def all_items():
    response_object = { 'status':'success' }
    if request.method == 'POST':
        post_data = request.get_json()
        ITEMS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'genre': post_data.get('genre'),
            'available': post_data.get('available')
        })
        response_object['message'] = 'Item Added!'
    else:
        response_object['items'] = ITEMS
        response_object['message'] = 'Item Loaded!'
    return jsonify(response_object)

@app.route('/items/<item_id>', methods=['PUT', 'DELETE'])
def single_item(item_id):
    response_object = { 'status': 'success' }
    if request.method == 'PUT':
        post_data = request.get_json()
        remove_item(item_id)
        ITEMS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'genre': post_data.get('genre'),
            'available': post_data.get('played')
        })
        response_object['message'] = 'Item Updated!'
    if request.method == 'DELETE':
        remove_item(item_id)
        response_object['message'] = 'Item Removed!️'
    return jsonify(response_object)

def remove_item(item_id):
    for item in ITEMS:
        if item['id'] == item_id:
            ITEMS.remove(item)
            return True
    return False

if __name__ =='__main__':
    app.run(debug=True)