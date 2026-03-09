import os
import logging
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException, Header, status
from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, Session, relationship
from sqlalchemy.sql import func

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[logging.FileHandler("production_api.log"),logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

engine = create_engine(os.getenv("DATABASE_URL"), pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    category = Column(String(100))
    price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class SaleTransaction(Base):
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    total_amount = Column(Float)
    transaction_date = Column(DateTime(timezone=True), server_default=func.now())
    
    product = relationship("Product")

Base.metadata.create_all(bind=engine)

class ProductBase(BaseModel):
    name: str
    category: str
    price: float = Field(gt=0, description="Price must be positive")
    stock_quantity: int = Field(ge=0)

class ProductCreate(ProductBase):
    pass

class ProductSchema(ProductBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class AnalyticsReport(BaseModel):
    total_revenue: float
    total_transactions: int
    best_selling_category: str
    low_stock_alerts: int

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def authenticate_role(x_api_key: str = Header(..., alias="X-API-KEY")):
    if x_api_key == os.getenv("ADMIN_KEY"):
        return "admin"
    if x_api_key == os.getenv("SELLER_KEY"):
        return "seller"
    if x_api_key == os.getenv("BUYER_KEY"):
        return "buyer"
    
    logger.error("Failed authentication attempt.")
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid credentials")

app = FastAPI(version="1.0.0")

@app.post("/inventory/add", response_model=ProductSchema, status_code=201)
def add_new_inventory(product_data: ProductCreate, db: Session = Depends(get_db),role: str = Depends(authenticate_role)):
    if role not in ["seller", "admin"]:
        raise HTTPException(403, "Insufficient permissions")
    
    new_item = Product(
        name=product_data.name,
        category=product_data.category,
        price=product_data.price,
        stock_quantity=product_data.stock_quantity
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    logger.info(f"Inventory added: {new_item.name} by {role}")
    return new_item

@app.get("/products/available")
def get_available_products(db: Session = Depends(get_db)):
    available_items = db.query(Product).filter(Product.stock_quantity > 0).all()
    
    if len(available_items) == 0:
        return {"message": "Sorry, all products are currently out of stock!"}
    else:
        return available_items

@app.post("/commerce/purchase/{product_id}")
def process_sale(product_id: int, qty: int = 1, db: Session = Depends(get_db),role: str = Depends(authenticate_role)):
    if role != "buyer":
        raise HTTPException(403, "Only buyers can checkout")

    product = db.query(Product).filter(Product.id == product_id).first()
    
    if not product or product.stock_quantity < qty:
        raise HTTPException(400, "Item unavailable or stock insufficient")

    product.stock_quantity = product.stock_quantity - qty
    
    sale = SaleTransaction(product_id=product.id,quantity=qty,unit_price=product.price,total_amount=product.price * qty)
    db.add(sale)
    db.commit()
    logger.info(f"Sale processed: {qty} units of {product.name}")
    return {"status": "success", "order_total": sale.total_amount}

@app.get("/analytics/dashboard", response_model=AnalyticsReport)
def generate_business_intelligence(db: Session = Depends(get_db), role: str = Depends(authenticate_role)):
    if role != "admin":
        raise HTTPException(403, "Admin authorization required")

    sales = db.query(SaleTransaction).all()
    products = db.query(Product).all()

    rev_total = 0
    category_map = {}
    low_stock_count = 0

    for s in sales:
        rev_total = rev_total + s.total_amount

    for p in products:
        if p.stock_quantity < 5:
            low_stock_count = low_stock_count + 1
        
        current_cat = p.category
        if current_cat not in category_map:
            category_map[current_cat] = 0
        category_map[current_cat] = category_map[current_cat] + 1

    top_cat = "N/A"
    max_count = 0
    for cat in category_map:
        if category_map[cat] > max_count:
            max_count = category_map[cat]
            top_cat = cat

    return {
        "total_revenue": rev_total,
        "total_transactions": len(sales),
        "best_selling_category": top_cat,
        "low_stock_alerts": low_stock_count
    }

