from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["creator_intelligence"]

products = list(db.products.find({"status": 1}))

for product in products:
    brand = product["brand"]
    product_name = product["product"]

    print(f"Brand: {brand}")
    print(f"Product: {product_name}")

    # Crawl here
