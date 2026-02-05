import io
from fastapi import APIRouter, UploadFile, File
from ultralytics import YOLO
from PIL import Image, ImageOps # 👈 Ajout de ImageOps pour la rotation

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
        # 1. Lire les octets
        image_bytes = await file.read()

        # 2. Ouvrir l'image
        image = Image.open(io.BytesIO(image_bytes))

        # 🔥 CORRECTION CRITIQUE : Remettre l'image à l'endroit
        # Les téléphones envoient souvent l'image tournée à 90°. Cette ligne la redresse.
        image = ImageOps.exif_transpose(image)
        
        # Sécurité couleur (au cas où ce soit du PNG transparent)
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # 3. Lancer la prédiction
        # On baisse le seuil à 0.25 (25%) pour être plus tolérant au début
        results = model.predict(image, conf=0.25)
        
        result = results[0] # Première image

        # --- ZONE DE DEBUG (Regarde ton terminal VPS !) ---
        print(f"📸 Image reçue. Objets détectés : {len(result.boxes)}")
        for box in result.boxes:
            d_class = model.names[int(box.cls)]
            d_conf = float(box.conf)
            print(f"   👀 Vu : {d_class} ({int(d_conf*100)}%)")
        # --------------------------------------------------

        if result.boxes:
            # On prend la meilleure détection
            box = result.boxes[0]
            class_id = int(box.cls)
            score = float(box.conf)
            label_name = model.names[class_id]

            return {
                "label": label_name, 
                "score": f"{int(score * 100)}%" 
            }
        
        else:
            return {"label": "Inconnu", "score": "0%"}

    except Exception as e:
        print(f"❌ Erreur critique analyse : {e}")
        return {"label": "Erreur", "score": "0%"}