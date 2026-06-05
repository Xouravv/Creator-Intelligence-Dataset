from db.config import products_collection
from datetime import datetime

products = [
    {
        "brand": "Apple",
        "product": "AirPods Pro 2",
        "status": 1,
        "created_at": datetime.utcnow()
    },
    {
        "brand": "Samsung",
        "product": "Galaxy Buds 3",
        "status": 1,
        "created_at": datetime.utcnow()
    },
    {
        "brand": "Sony",
        "product": "WH-1000XM5",
        "status": 1,
        "created_at": datetime.utcnow()
    }
]

products_collection.insert_many(products)

print("Products inserted")