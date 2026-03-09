from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, Session
from pydantic import BaseModel, Field

DATABASE_URL = "mysql+pymysql://root:root@localhost/fastapi_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    cart_items = relationship("Cart", back_populates="user")

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    price = Column(Float)
    stock = Column(Integer)

class Cart(Base):
    __tablename__ = "cart"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    user = relationship("User", back_populates="cart_items")
    product = relationship("Product")

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user_id():
    return 1  

class UserCreate(BaseModel):
    name: str

class ProductCreate(BaseModel):
    name: str
    price: float = Field(gt=0)
    stock: int = Field(ge=0)

class CartCreate(BaseModel):
    product_id: int
    quantity: int

@app.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(name=user.name) 
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/products/")
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    new_product = Product(name=product.name, price=product.price, stock=product.stock)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@app.get("/products/available")
def get_available_products(db: Session = Depends(get_db)):
    available_items = db.query(Product).filter(Product.stock > 0).all()
    
    if len(available_items) == 0:
        return {"message": "Out of stock!"}
    
    return available_items

@app.post("/cart/add")
def add_to_cart(item: CartCreate, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    product = db.query(Product).filter(Product.id == item.product_id).first()
    if not product:
        raise HTTPException(404, "Product not found")

    if product.stock < item.quantity:
        raise HTTPException(400, "Not enough stock")

    cart_item = db.query(Cart).filter(Cart.user_id == user_id, Cart.product_id == item.product_id).first()

    if cart_item:
        cart_item.quantity = cart_item.quantity + item.quantity
    else:
        cart_item = Cart(user_id=user_id, product_id=item.product_id, quantity=item.quantity)
        db.add(cart_item)

    product.stock = product.stock - item.quantity
    db.commit()
    return {"message": "Added to cart"}

@app.get("/cart/my-cart")
def view_cart(db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    cart_items = db.query(Cart).filter(Cart.user_id == user_id).all()

    if not cart_items:
        return {"message": "Cart is empty", "items": [], "total": 0}

    result = []
    total = 0

    for item in cart_items:
        line_total = item.quantity * item.product.price
        total = total + line_total
        result.append({
            "product": item.product.name,
            "price": item.product.price,
            "quantity": item.quantity,
            "total": line_total
        })

    return {"items": result, "cart_total": total}

@app.delete("/cart/remove/{product_id}")
def remove_from_cart(product_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    item = db.query(Cart).filter(Cart.user_id == user_id, Cart.product_id == product_id).first()

    if not item:
        raise HTTPException(404, "Item not in cart")
    product = db.query(Product).filter(Product.id == product_id).first()
    product.stock = product.stock + item.quantity

    db.delete(item)
    db.commit()
    return {"message": "Item removed and stock restored"}

@app.delete("/cart/clear")
def clear_cart(db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    items = db.query(Cart).filter(Cart.user_id == user_id).all()

    for item in items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        product.stock = product.stock + item.quantity
        db.delete(item)

    db.commit()
    return {"message": "Cart cleared"}