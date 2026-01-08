from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from datetime import datetime # 👈 Pour la date
import os
import shutil
import json
from uuid import uuid4


DATASET_DIR = "dataset_raw"
os.makedirs(DATASET_DIR, exist_ok=True)

router = APIRouter()

@router.post("/contribute")
async def contribute_image(
    file: UploadFile = File(...), 
    label: str = Form(...), 
    user_id: str = Form(...), 
    bbox: str = Form(...)
):  
    try:
        clean_label = label.lower().strip().replace(" ", "_")
        
        save_dir = os.path.join(DATASET_DIR, clean_label)
        os.makedirs(save_dir, exist_ok=True)
        
        unique_id = str(uuid4())
        image_filename = f"{unique_id}.jpg"
        annotation_filename = f"{unique_id}.json"
        
        image_path = os.path.join(save_dir, image_filename)
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        bbox_data = json.loads(bbox)
        
        annotation_data = {
            "image_id": unique_id,
            "user_id": user_id,
            "label": clean_label,
            "bbox": bbox_data,
            "timestamp": datetime.now().isoformat() 
        }
        
        annotation_path = os.path.join(save_dir, annotation_filename)
        with open(annotation_path, "w") as f:
            json.dump(annotation_data, f, indent=4)
            
        print(f"✅ Contribution reçue : {clean_label} (ID: {unique_id})")
        return {"message": "Contribution enregistrée avec succès !"}

    except Exception as e:
        print(f"❌ Erreur lors de la contribution : {e}")
        raise HTTPException(status_code=500, detail="Erreur interne serveur lors de la sauvegarde")