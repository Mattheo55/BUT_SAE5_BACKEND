import base64
import cv2
from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel
from ultralytics import YOLO

app = APIRouter()

try:
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

            img_with_box = result.plot()

            _, buffer = cv2.imencode('.jpg', img_with_box)

            img_base64 = base64.b64encode(buffer).decode('utf-8')

            return {
                "label": best_label,
                "score": f"{best_score}%",
                "annoted_image": img_base64,
            }
        
        else:
            return {
                "label": "Inconnu",
                "score": "0%"
            }

    except Exception as e:
        print(f"Erreur API: {e}")
        raise HTTPException(status_code=500, detail=str(e))

