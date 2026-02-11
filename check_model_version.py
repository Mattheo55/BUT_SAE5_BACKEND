import os
from fastapi import APIRouter
from fastapi.responses import FileResponse

app = APIRouter()

@app.get("/check_model_version")
def check_model_version():
    return {
        "version": '1.0.0',
        "download_url": "http://51.77.146.102/IA/best.tflite"
    }

@app.get('/IA/best.tflite')
def download():
    file_path = "IA/best_float16.tflite"

    if os.path.exists(file_path):
        return FileResponse(file_path, media_type='application/octet-stream', filename='best_float16.tflite')
    return {
        "error": "Fichier non trouve"
    }