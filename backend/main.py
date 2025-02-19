from fastapi import FastAPI, File, UploadFile
import os
import shutil
from face_recog_system.face_recog import recognize_face  # Updated import after renaming

app = FastAPI()

UPLOAD_DIR = "face_recog_system/uploads/"  # Ensure this matches your updated folder name

# Ensure the uploads folder exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/recognize-face/")
async def recognize(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Save the uploaded file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Process the image
    result = recognize_face(file_path)
    return {"name": result}
