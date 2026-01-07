from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from ultralytics import YOLO

# On utilise 'app' par convention, pas 'router' (sauf si c'est un sous-fichier)
app = FastAPI()

# Chargement du modèle (une seule fois au démarrage)
try:
    # Assure-toi que le dossier 'IA' est au même niveau que ce fichier python
    model = YOLO('IA/best.pt') 
    print("✅ Modèle chargé avec succès !")
except Exception as e:
    print(f"❌ Erreur chargement modèle : {e}")

class ImageRequest(BaseModel):
    image_url: str

@app.post('/analyze_animal')
async def analyze_animal(request: ImageRequest):
    try:
        results = model(request.image_url)
        
        result = results[0]

        
        if result.boxes:
            best_conf = -1.0
            best_cls_id = -1

            for box in result.boxes:
                conf = float(box.conf)
                if conf > best_conf:
                    best_conf = conf
                    best_cls_id = int(box.cls)

            best_label = result.names[best_cls_id]
            best_score = round(best_conf * 100)

            return {
                "label": best_label,
                "score": f"{best_score}%"
            }
        
        else:
            return {
                "label": "Inconnu",
                "score": "0%"
            }

    except Exception as e:
        print(f"Erreur API: {e}")
        raise HTTPException(status_code=500, detail=str(e))

