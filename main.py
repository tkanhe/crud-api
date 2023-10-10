import configparser
import csv

from fastapi import FastAPI, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

# Load MongoDB configuration from config.ini
config = configparser.ConfigParser()
config.read("config.ini")

mongo_config = config["MongoDB"]

app = FastAPI()


# Get the MongoDB collection
def get_collection():
    try:
        client = MongoClient(
            host=mongo_config["host"],
            port=int(mongo_config["port"]),
        )
        db = client[mongo_config["database"]]
        collection = db[mongo_config["collection"]]
        return collection

    except Exception as e:
        print("ERROR: An exception occurred while connecting to MongoDB: ", repr(e))
        raise e


# Import data from CSV file to MongoDB at startup
@app.on_event("startup")
def import_data_from_csv():
    collection = get_collection()
    if collection.count_documents({}) != 0:
        collection.delete_many({})

    with open("data.csv", "r") as f:
        csv_data = csv.DictReader(f)
        for row in csv_data:
            product = {
                "_id": row["id"],
                "name": row["name"],
                "description": row["description"],
                "price": float(row["price"]),
                "category": row["category"],
            }

            collection.insert_one(product)

    print("Data imported successfully")


class Product(BaseModel):
    id: str = Field(alias="_id")
    name: str
    description: str
    price: float
    category: str

    class Config:
        populate_by_name = True


class ProductUpdate(BaseModel):
    name: str
    description: str
    price: float
    category: str


# Route to create a new product
@app.post("/products/")
def create_product(product: Product, collection=Depends(get_collection)):
    try:
        product_data = jsonable_encoder(product)
        result = collection.insert_one(product_data)
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Product already exists")
    res = {"message": "Product created successfully", "_id": str(result.inserted_id)}
    return JSONResponse(status_code=201, content=res)


# Route to get a list of all products
@app.get("/products/")
def get_all_products(collection=Depends(get_collection)):
    products = collection.find()
    return list(products)


# Route to get a specific product by id
@app.get("/products/{product_id}")
def get_product(product_id: str, collection=Depends(get_collection)):
    product = collection.find_one({"_id": product_id})
    if product:
        return product
    raise HTTPException(status_code=404, detail="Product not found")


# Route to update a specific product by id
@app.put("/products/{product_id}")
def update_product(product_id: str, product: ProductUpdate, collection=Depends(get_collection)):
    product_data = jsonable_encoder(product)
    result = collection.update_one({"_id": product_id}, {"$set": product_data})
    if result.modified_count == 1:
        return {"message": "Product updated successfully"}
    raise HTTPException(status_code=404, detail="Product not found")


# Route to delete a product by id
@app.delete("/products/{product_id}")
def delete_product(product_id: str, collection=Depends(get_collection)):
    result = collection.delete_one({"_id": product_id})
    if result.deleted_count == 1:
        return {"message": "Product deleted successfully"}
    raise HTTPException(status_code=404, detail="Product not found")
