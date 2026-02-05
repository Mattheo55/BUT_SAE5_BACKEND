import io
from fastapi import APIRouter, UploadFile, File
from ultralytics import YOLO
from PIL import Image, ImageOps

app = APIRouter()

# On charge le modèle une seule fois au démarrage
try:
    model = YOLO('IA/best.pt') 
    print("✅ MOTEUR IA PRÊT (Mode Rapide)")
except Exception as e:
    print(f"❌ Erreur modèle : {e}")

@app.post('/analyze_file_direct')
async def analyze_file_direct(file: UploadFile = File(...)):
    try:
        # 1. Lecture ultra-rapide
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes))

        # 2. On redresse l'image (Sinon l'IA voit l'animal couché)
        image = ImageOps.exif_transpose(image)
        
        # 3. Prédiction (Seuil bas pour réactivité)
        results = model.predict(image, conf=0.25, imgsz=320) # imgsz=320 accélère l'IA
        result = results[0]

        if result.boxes:
            # On prend juste le premier résultat
            box = result.boxes[0] 
            
            # 🔥 LE SECRET DE LA STABILITÉ : .item()
            class_id = int(box.cls.item()) 
            score = float(box.conf.item())
            
            label_name = result.names[class_id]
            
            # On log juste pour le debug
            print(f"⚡️ Vu : {label_name} ({int(score*100)}%)")

            return {
                "label": label_name, 
                "score": f"{int(score * 100)}%" 
            }
        
        return {"label": "Inconnu", "score": "0%"}

    except Exception as e:
        print(f"❌ Erreur: {e}")
        return {"label": "Erreur", "score": "0%"}