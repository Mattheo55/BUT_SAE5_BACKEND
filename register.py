from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr

router = APIRouter()
pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

class UserCreate(BaseModel):
    email: EmailStr
    name: str
    password: str

@router.post('/register', status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Cet email est déjà enregistré"
        )
    
    hashed_pwd = pwd_context.hash(user_data.password)

    new_user = User(
        email=user_data.email,
        name=user_data.name,
        hashed_password=hashed_pwd,
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {
            "message": "Compté créé avec succès",
            "user_id": new_user.id,
            "user_name": new_user.name,
            "user_email": new_user.email
        }
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Erreur lors de l'enregistrement")