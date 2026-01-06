from warnings import deprecated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt

SECRET_KEY = "EGVESZG4BSR4G4ESRG85ES"
ALGORITHM = "HS256"

def create_access_token(data: dict):
    to_encode = data.copy()
    
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

router = APIRouter()
pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

class LoginSchema(BaseModel):
    email: str
    password: str

@router.post("/login")
def login(data: LoginSchema, db: Session=Depends(get_db)):
    
    db_user = db.query(User).filter(User.email == data.email).first()

    if not db_user or not pwd_context.verify(data.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Identifiants incorrect")
    
    access_token = create_access_token(data={"sub": db_user.email})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": db_user.id,
        "user_email": db_user.email,
        "user_name": db_user.name,
        "message": "Connexion réussie"
    }