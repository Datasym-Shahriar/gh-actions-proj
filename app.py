from flask import Flask, jsonify, request

app = Flask(__name__)

# Initial data for stores
stores = [
    {
        "name": "My Store",
        "items": [
            {"name": "iPhone", "price": 1099.99},
            {"name": "MacBook", "price": 1999.99}
        ],
        "franchise": False
    },
    {
        "name": "Your Store",
        "items": [
            {"name": "Galaxy S21", "price": 799.99},
            {"name": "Surface Pro", "price": 1299.99}
        ],
        "franchise": True
    }
]

@app.route('/store', methods=['GET'])
def get_stores():
    """
    Returns a list of all stores.
    """
    return jsonify(stores=stores)

@app.route('/store', methods=['POST'])
def create_store():
    """
    Creates a new store.
    The request body must be a JSON object with a "name" key.
    An "items" key is optional and defaults to an empty list.
    A "franchise" key is optional and defaults to False.
    """
    # Get JSON data from the request, returns None if parsing fails or mimetype is not application/json
    request_data = request.get_json(silent=True)

    # Error handling for missing or invalid JSON payload
    if request_data is None:
        return jsonify(error="Invalid JSON or no input data provided."), 400

    # Check for the presence of the required 'name' field
    store_name = request_data.get('name')
    if not store_name:
        return jsonify(error="'name' field is required."), 400

    # Check if a store with the same name already exists
    for store in stores:
        if store['name'] == store_name:
            return jsonify(error=f"Store with name '{store_name}' already exists."), 409 # 409 Conflict

    # Create the new store object
    new_store = {
        "name": store_name,
        "items": request_data.get("items", []), # Default to an empty list if not provided
        "franchise": request_data.get("franchise", False) # Default to False if not provided
    }

    # Add the new store to our list
    stores.append(new_store)

    # Return the newly created store with a 201 Created status code
    return jsonify(new_store), 201

# To run this app, save it as app.py and run `flask run` in your terminal.
# Ensure you have Flask installed: `pip install Flask`
