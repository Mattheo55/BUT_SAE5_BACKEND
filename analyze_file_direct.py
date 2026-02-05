import io
from fastapi import APIRouter, UploadFile, File
from ultralytics import YOLO
from PIL import Image

app = APIRouter()

# Chargement du modèle
try:
    model = YOLO('IA/best.pt') 
    print("✅ Modèle chargé avec succès !")
except Exception as e:
    print(f"❌ Erreur chargement modèle : {e}")

@app.post('/analyze_file_direct')
async def analyze_file_direct(file: UploadFile = File(...)):
    try:
        # 1. Lire les octets du fichier envoyé par le téléphone
        image_bytes = await file.read()

        # 2. Convertir les octets en Image PIL (que YOLO peut comprendre)
        image = Image.open(io.BytesIO(image_bytes))

        # 3. Lancer la prédiction
        # conf=0.4 : On ignore tout ce qui est en dessous de 40% de certitude
        results = model.predict(image, conf=0.4)
        
        # 4. Analyser le résultat
        result = results[0] # On prend la première (et seule) image

        if result.boxes:
            # On prend la boîte avec le meilleur score (la première)
            box = result.boxes[0]
            
            # Récupérer l'ID de la classe (ex: 0, 1, 2)
            class_id = int(box.cls)
            
            # Récupérer le score (ex: 0.85)
            score = float(box.conf)
            
            # Récupérer le nom (ex: "Ours") grâce au dictionnaire du modèle
            label_name = model.names[class_id]

            return {
                "label": label_name, 
                "score": f"{int(score * 100)}%" 
            }
        
        else:
            # Rien n'a été détecté
            return {"label": "Inconnu", "score": "0%"}

    except Exception as e:
        print(f"Erreur analyse : {e}")
        return {"label": "Erreur", "score": "0%"}