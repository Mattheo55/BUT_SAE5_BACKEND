from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc, null
from database import get_db
from models.history import History

router = APIRouter()

@router.get('/last_history')
def get_last_history(user_id: int, db: Session=Depends(get_db)):
    
    last_history = db.query(History).filter(History.user_id == user_id).order_by(desc(History.id)).first()

    if not last_history:
        return null

    return last_history