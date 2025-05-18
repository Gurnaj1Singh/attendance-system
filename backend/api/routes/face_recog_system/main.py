from fastapi import APIRouter, File, UploadFile
import os
import shutil
from backend.api.routes.face_recog_system.face_recog import recognize_face  

router = APIRouter()
    
UPLOAD_DIR = "backend/api/routes/face_recog_system/uploads"
absolute_path = os.path.abspath(UPLOAD_DIR)
print(f"📂 UPLOAD_DIR is expected at: {absolute_path}")

# Ensure the uploads folder exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/recognize-face/")
async def recognize(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Save the uploaded file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Process the image
    result = recognize_face(file_path)
    return {"name": result}
    

