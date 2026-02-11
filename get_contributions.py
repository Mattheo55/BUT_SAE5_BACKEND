from fastapi import APIRouter, Depends, HTTPException 
from sqlalchemy import desc
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import Base, get_db
from models.contributions import Contribution
from models.history import History

router = APIRouter()

@router.get('/get_contributions')
def get_contributions(user_id: int, db: Session=Depends(get_db)):
    
    history_list = db.query(Contribution).filter(Contribution.user_id == user_id).order_by(desc(Contribution.id)).all()

    if not history_list:
        return []
    
    return history_list