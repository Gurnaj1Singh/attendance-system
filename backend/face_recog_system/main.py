from fastapi import FastAPI, File, UploadFile
import os
from fastapi.middleware.cors import CORSMiddleware

import shutil
from face_recog import recognize_face  # Updated import after renaming

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ✅ Allow all origins (or specify your frontend URL)
    allow_credentials=True,
    allow_methods=["*"],  # ✅ Allow all HTTP methods
    allow_headers=["*"],  # ✅ Allow all headers
)
    
UPLOAD_DIR = "backend/face_recog_system/uploads/"  # Ensure this matches your updated folder name
absolute_path = os.path.abspath(UPLOAD_DIR)
print(f"📂 UPLOAD_DIR is expected at: {absolute_path}")

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
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)

