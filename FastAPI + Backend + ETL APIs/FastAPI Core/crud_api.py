from fastapi import FastAPI
from models import Product

app=FastAPI()

@app.get("/")
def test():
    return {"hello"}

products = [
    Product(id=1,name="Phone",description="A smart phone",price=699.99,quantity=50),
    Product(id=2,name="Laptop",description="A Laptop",price=999.99,quantity=30)
]

@app.get("/product")
def get_all_product():
    return products

@app.get("/product/{id}")
def get_product(id: int):
    for product in products:
        if product.id == id:
            return product
    return {"Product not found"}

@app.post("/product")
def add_product(product: Product):
    products.append(product)
    return product

@app.put("/product")
def update_product(id: int, product: Product):
    for i in range(len(products)):
        if products[i].id == id:
            products[i] = product
            return {"Product added sucessfully"}
    return {"No product found"}

@app.delete("/product")
def delete_product(id: int):
    for i in range(len(products)):
        if products[i].id == id:
            del products[i]
            return {"Product deleted sucessfully"}
    return {"No product found"}