from fastapi import APIRouter, Depends, HTTPException 
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from models.contributions import Contribution

router = APIRouter()

class ContributionModel(BaseModel):
    user_id: int
    animale_name : str
    uri: str


@router.post("/add_contribution")
def addContribution(data: ContributionModel, db: Session=Depends(get_db)):

    new_history = Contribution(
        user_id=data.user_id,
        animale_name=data.animale_name,
        uri=data.uri
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
        raise HTTPException(status_code=500, detail="Une erreure c'est produit lors de l'ajouter d'un element de l'historique de contribution dans la bdd")