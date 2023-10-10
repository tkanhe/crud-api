import json

from fastapi.testclient import TestClient

from main import app, get_collection

client = TestClient(app)


def test_mongodb_connection():
    test_collectionx = get_collection()
    assert test_collectionx.count_documents({}) != 0


# Define the MongoDB collection for testing
test_collection = get_collection()


def test_create_product():
    # delete _id if exists
    product_id = "test_id10"
    test_collection.delete_one({"_id": product_id})
    assert test_collection.find_one({"_id": product_id}) is None

    # Test create product
    product_data = {
        "_id": product_id,
        "name": "Test name",
        "description": "Test description",
        "price": 10.10,
        "category": "Test category",
    }
    response = client.post("/products/", json=product_data)
    assert response.status_code == 201
    assert "Product created successfully" in response.text
    product_id = json.loads(response.text)["_id"]

    # Error case: Test duplicate product creation
    response = client.post("/products/", json=product_data)
    assert response.status_code == 400
    assert "Product already exists" in response.text

    # Clean up: Delete the test product
    response = client.delete(f"/products/{product_id}")
    assert response.status_code == 200
    assert "Product deleted successfully" in response.text


def test_get_all_products():
    # Test get all products
    response = client.get("/products/")
    assert response.status_code == 200
    assert isinstance(json.loads(response.text), list)


def test_get_product():
    # delete _id if exists
    product_id = "test_id10"
    test_collection.delete_one({"_id": product_id})
    assert test_collection.find_one({"_id": product_id}) is None

    # Test create product
    product_data = {
        "_id": product_id,
        "name": "Test name",
        "description": "Test description",
        "price": 10.10,
        "category": "Test category",
    }
    response = client.post("/products/", json=product_data)
    assert response.status_code == 201
    assert "Product created successfully" in response.text
    product_id = json.loads(response.text)["_id"]

    # Test get product
    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200

    # Error case: Test get product
    response = client.get(f"/products/{product_id}1")
    assert response.status_code == 404

    # Clean up: Delete the test product
    response = client.delete(f"/products/{product_id}")
    assert response.status_code == 200
    assert "Product deleted successfully" in response.text


def test_update_product():
    # delete _id if exists
    product_id = "test_id10"
    test_collection.delete_one({"_id": product_id})
    assert test_collection.find_one({"_id": product_id}) is None

    # Test create product
    product_data = {
        "_id": product_id,
        "name": "Test name",
        "description": "Test description",
        "price": 10.10,
        "category": "Test category",
    }
    response = client.post("/products/", json=product_data)
    assert response.status_code == 201
    assert "Product created successfully" in response.text
    product_id = json.loads(response.text)["_id"]

    # Test update product
    update_data = {
        "name": "Updated name",
        "description": "Updated description",
        "price": 10,
        "category": "Updated category",
    }
    response = client.put(f"/products/{product_id}", json=update_data)
    assert response.status_code == 200
    assert "Product updated successfully" in response.text

    # Clean up: Delete the test product
    response = client.delete(f"/products/{product_id}")
    assert response.status_code == 200
    assert "Product deleted successfully" in response.text


def test_delete_product():
    # delete _id if exists
    product_id = "test_id10"
    test_collection.delete_one({"_id": product_id})
    assert test_collection.find_one({"_id": product_id}) is None

    # Test create product
    product_data = {
        "_id": product_id,
        "name": "Test name",
        "description": "Test description",
        "price": 10.10,
        "category": "Test category",
    }
    response = client.post("/products/", json=product_data)
    assert response.status_code == 201
    assert "Product created successfully" in response.text
    product_id = json.loads(response.text)["_id"]

    # Test delete product
    response = client.delete(f"/products/{product_id}")
    assert response.status_code == 200
    assert "Product deleted successfully" in response.text

    # Clean up: Ensure the test product is deleted
    assert test_collection.find_one({"_id": product_id}) is None
