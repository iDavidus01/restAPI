from flask import Flask, jsonify, request

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

@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = next((user for user in users if user['id'] == id), None)
    if user:
        return jsonify(user), 200
    return jsonify({'message': 'User not found'}), 404

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or "name" not in data or "lastname" not in data:
        return jsonify({'message': 'Invalid data'}), 400

    new_id = max([user['id'] for user in users]) + 1
    new_user = {"id": new_id, "name": data['name'], "lastname": data['lastname']}
    users.append(new_user)
    return jsonify(new_user), 201

@app.route('/users/<int:id>', methods=['PATCH'])
def update_user(id):
    user = next((user for user in users if user['id'] == id), None)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    data = request.get_json()
    if not data or ("name" not in data and "lastname" not in data):
        return jsonify({"error": "Invalid input"}), 400

    if "name" in data:
        user["name"] = data["name"]
    if "lastname" in data:
        user["lastname"] = data["lastname"]

    return "", 204

@app.route('/users/<int:id>', methods=['PUT'])
def replace_user(id):
    user = next((user for user in users if user['id'] == id), None)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    data = request.get_json()
    if not data or "name" not in data or "lastname" not in data:
        return jsonify({'message': 'Invalid data'}), 400

    user["name"] = data["name"]
    user["lastname"] = data["lastname"]

    return "", 204

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = next((user for user in users if user['id'] == id), None)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    users.remove(user)
    return "", 204


if __name__ == '__main__':
    app.run(debug=True)