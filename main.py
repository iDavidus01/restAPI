from flask import Flask, jsonify

app = Flask(__name__)

users = [
    {"id": 1, "name": "Wojciech", "lastname": "Oczkowski"},
    {"id": 2, "name": "John", "lastname": "Doe"}
]

@app.route('/')
def home():
    return jsonify({'message': 'server on'})

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users), 200

if __name__ == '__main__':
    app.run(debug=True)