import pytest
import json
from app import app, stores

@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        # Reset the stores list before each test to ensure isolation
        stores[:] = [
            {
                "name": "My Store",
                "items": [{"name": "iPhone", "price": 1099.99}],
                "franchise": False
            }
        ]
        yield client

def test_get_stores(client):
    """
    Test the GET /store endpoint.
    It should return all stores and a 200 OK status.
    """
    response = client.get('/store')
    data = json.loads(response.data)

    assert response.status_code == 200
    assert "stores" in data
    assert len(data["stores"]) == 1
    assert data["stores"][0]["name"] == "My Store"

def test_create_store_success(client):
    """
    Test the POST /store endpoint for a successful creation with all data.
    """
    new_store_data = {
        "name": "New Awesome Store",
        "items": [{"name": "Laptop", "price": 1500}],
        "franchise": True
    }
    response = client.post('/store', data=json.dumps(new_store_data), content_type='application/json')
    data = json.loads(response.data)

    assert response.status_code == 201
    assert data['name'] == "New Awesome Store"
    assert "items" in data
    assert len(data['items']) == 1
    assert data['franchise'] is True
    assert len(stores) == 2 # Check that the global stores list was updated

def test_create_store_without_items(client):
    """
    Test creating a store with only a name. Items should default to an empty list.
    """
    new_store_data = {"name": "Just a Name Store"}
    response = client.post('/store', data=json.dumps(new_store_data), content_type='application/json')
    data = json.loads(response.data)

    assert response.status_code == 201
    assert data['name'] == "Just a Name Store"
    assert data['items'] == []
    assert data['franchise'] is False # Check default value
    assert len(stores) == 2

def test_create_store_duplicate_name(client):
    """
    Test that creating a store with a duplicate name returns a 409 Conflict error.
    """
    duplicate_store_data = {"name": "My Store"}
    response = client.post('/store', data=json.dumps(duplicate_store_data), content_type='application/json')
    data = json.loads(response.data)

    assert response.status_code == 409
    assert "error" in data
    assert "already exists" in data["error"]
    assert len(stores) == 1 # Ensure no new store was added

def test_create_store_no_json_body(client):
    """
    Test POST /store with no JSON body. Should return a 400 Bad Request.
    """
    response = client.post('/store', content_type='application/json') # No data
    data = json.loads(response.data)

    assert response.status_code == 400
    assert "error" in data
    assert "no input data provided" in data["error"]

def test_create_store_empty_json(client):
    """
    Test POST /store with an empty JSON object. Should return a 400 error.
    """
    response = client.post('/store', data=json.dumps({}), content_type='application/json')
    data = json.loads(response.data)

    assert response.status_code == 400
    assert "error" in data
    assert "'name' field is required" in data["error"]

def test_create_store_no_name_field(client):
    """
    Test POST /store with JSON that is missing the 'name' field. Should return a 400 error.
    """
    bad_data = {"items": []} # Missing name
    response = client.post('/store', data=json.dumps(bad_data), content_type='application/json')
    data = json.loads(response.data)

    assert response.status_code == 400
    assert "error" in data
    assert "'name' field is required" in data["error"]

# To run these tests, save the file as test_app.py and run `pytest` in your terminal.
# Ensure you have pytest installed: `pip install pytest`
