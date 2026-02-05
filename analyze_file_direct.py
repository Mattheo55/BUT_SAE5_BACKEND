import io
from fastapi import APIRouter, UploadFile, File
from ultralytics import YOLO
from PIL import Image, ImageOps 

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

        # Redressement image
        image = ImageOps.exif_transpose(image)
        
        # Sécurité couleur
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # 3. Prédiction (Seuil à 0.25)
        results = model.predict(image, conf=0.25)
        
        result = results[0]

        # Debug console
        print(f"📸 Image reçue. Objets détectés : {len(result.boxes)}")
        for box in result.boxes:
             d_class = model.names[int(box.cls.item())] # Correction ici aussi pour le print
             d_conf = float(box.conf.item())
             print(f"   👀 Vu : {d_class} ({int(d_conf*100)}%)")

        if result.boxes:
            # On prend la meilleure détection
            box = result.boxes[0]
            
            # 🔥 CORRECTION CRITIQUE ICI 🔥
            # On utilise .item() pour éviter le crash serveur
            class_id = int(box.cls.item()) 
            score = float(box.conf.item())
            
            label_name = model.names[class_id]

            print(f"🦊 DÉTECTÉ ET ENVOYÉ : {label_name}")

            return {
                "label": label_name, 
                "score": f"{int(score * 100)}%" 
            }
        
        else:
            return {"label": "Inconnu", "score": "0%"}

    except Exception as e:
        # Affiche l'erreur réelle dans le terminal
        print(f"❌ CRASH SERVEUR : {e}")
        return {"label": "Erreur", "score": "0%"}