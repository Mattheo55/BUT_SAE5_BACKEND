from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from jose import jwt, JWTError
from datetime import datetime, timezone

router = APIRouter()

SECRET_KEY = "EGVESZG4BSR4G4ESRG85ES"
ALGORITHM = "HS256"

@router.get("/me")
def get_me(authorization: str = Header(None), db: Session = Depends(get_db)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token manquant ou format invalide")
    
    try:
        token = authorization.split(" ")[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        user_email: str = payload.get("sub")
        
        if user_email is None:
            raise HTTPException(status_code=401, detail="Token invalide : email manquant")

        user = db.query(User).filter(User.email == user_email).first()
        
        if user is None:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

        return {
            "id": user.id,
            "email": user.email,
            "name": user.name
        }

    except JWTError:
        raise HTTPException(status_code=401, detail="Session expirée ou jeton corrompu")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")