import os
import logging
from datetime import datetime, timedelta
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from sqlalchemy.exc import SQLAlchemyError
from passlib.context import CryptContext
from jose import jwt, JWTError
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-for-dev")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
EXPIRE_MINS = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[logging.FileHandler("app.log")]
)
logger = logging.getLogger("API")

engine = create_engine(
    "mysql+pymysql://root:root@localhost/analytics_api", 
    pool_pre_ping=True, 
    pool_recycle=3600
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), default="user")

Base.metadata.create_all(bind=engine)

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    role: str = "user"

class Token(BaseModel):
    access_token: str
    token_type: str

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/login")

def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=EXPIRE_MINS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid or expired",headers={"WWW-Authenticate": "Bearer"})

def require_role(allowed_roles: list):
    def role_checker(user=Depends(get_current_user)):
        user_role = user.get("role")
        
        role_allowed = False
        for role in allowed_roles:
            if user_role == role:
                role_allowed = True
        
        if not role_allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="Access denied: Permissions denied"
            )
        return user
    return role_checker

app = FastAPI(version="1.0.1")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = datetime.now()
    response = await call_next(request)
    duration = datetime.now() - start_time
    logger.info(f"{request.method} {request.url} | Status: {response.status_code} | Duration: {duration}")
    return response

@app.post("/v1/signup", status_code=201)
def signup(user_in: UserCreate, db: Session = Depends(get_db)):
    try:
        existing = db.query(User).filter(User.email == user_in.email).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")

        new_user = User(email=user_in.email, hashed_password=pwd_context.hash(user_in.password), role=user_in.role)
        db.add(new_user)
        db.commit()
        logger.info(f"User created: {user_in.email}")
        return {"status": "success", "detail": "User created successfully"}
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Internal database error")

@app.post("/v1/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == form_data.username).first()
    
    if not db_user or not pwd_context.verify(form_data.password, db_user.hashed_password):
        logger.warning(f"Login failed for: {form_data.username}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid email or password")

    token = create_token({"sub": db_user.email, "role": db_user.role})
    logger.info(f"Login successful: {db_user.email}")
    return {"access_token": token, "token_type": "bearer"}

@app.get("/v1/admin-only", dependencies=[Depends(require_role(["admin"]))])
def admin_dashboard():
    return {"data": "admin authorized access only."}