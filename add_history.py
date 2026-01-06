from fastapi import APIRouter, Depends, HTTPException 
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from models.history import History

router = APIRouter()

class HistoryModel(BaseModel):
    user_id: int
    animale_name : str
    animale_rate_reconize : int


@router.post("/add_history")
def addHistory(data: HistoryModel, db: Session=Depends(get_db)):

    new_history = History(
        user_id=data.user_id,
        animale_name=data.animale_name,
        animale_rate_reconize=data.animale_rate_reconize,
    )

    try:
        db.add(new_history)
        db.commit()
        db.refresh(new_history)

        return {
            "message": "Ajout avec succés"
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Une erreu c'est produit lors de l'ajouter d'un element de l'historique dans la bdd")