from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "admin": "1234",
    "user": "password"
}

catalog = {
    1: {"name": "Shirt", "price": 20, "size": "M", "color": "Red"},
    2: {"name": "Pants", "price": 40, "size": "L", "color": "Black"}
}


@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username


@app.route('/items', methods=['GET', 'POST'])
@auth.login_required
def items():
    if request.method == 'GET':
        return jsonify(catalog)

    if request.method == 'POST':
        data = request.json
        if not data or "name" not in data or "price" not in data or "size" not in data or "color" not in data:
            return jsonify({"error": "Invalid data"}), 400

        new_id = max(catalog.keys()) + 1 if catalog else 1
        catalog[new_id] = {
            "name": data["name"],
            "price": data["price"],
            "size": data["size"],
            "color": data["color"]
        }
        return jsonify({"message": "Item added", "id": new_id}), 201

if __name__ == '__main__':
    app.run(debug=True)
