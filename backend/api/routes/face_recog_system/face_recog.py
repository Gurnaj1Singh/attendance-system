import face_recognition, cv2, json, os
import numpy as np
from backend.database.db_connection import engine
from backend.database.models import Student
from sqlalchemy.orm import sessionmaker

DATASET_PATH = "backend/api/routes/face_recog_system/dataset"
absolute_path = os.path.abspath(DATASET_PATH)
print(f"UPLOAD_DIR is expected at: {absolute_path}")
print(f"Checking dataset path: {os.path.abspath(DATASET_PATH)}")

# SQLAlchemy session setup
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

def encode_faces_to_db():
    if not os.path.exists(DATASET_PATH):
        print("❌ Dataset folder not found! Create 'dataset/' and add images.")
        return

    files_processed = 0
    faces_encoded = 0

    for file in os.listdir(DATASET_PATH):
        if file.endswith(".jpg") or file.endswith(".png"):
            files_processed += 1
            image_path = os.path.join(DATASET_PATH, file)
            print(f"📷 Processing: {image_path}")

            # Extract name from filename (e.g., john@example.com.jpg)
            name_from_file = file.split(".")[0]

            # Find student by email or name (customize as needed)
            student = db.query(Student).filter(Student.name == name_from_file).first()
            if not student:
                print(f"⚠️ No student found for: {name_from_file}")
                continue

            image = cv2.imread(image_path)
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            face_locations = face_recognition.face_locations(rgb_image)
            face_encodings = face_recognition.face_encodings(rgb_image, face_locations)

            if face_encodings:
                encoding = face_encodings[0]
                student.face_data = json.dumps(encoding.tolist())  # Save as JSON string
                db.commit()
                faces_encoded += 1
                print(f"✅ Face encoding stored for: {student.name}")
            else:
                print(f"❌ No face detected in: {file}")

    db.close()
    print(f"\n🎉 Done! {faces_encoded} out of {files_processed} files processed and saved.")

# Run the function
encode_faces_to_db()

def recognize_face(image_path: str):
    print(f"📂 Recognizing face from image: {os.path.abspath(image_path)}")

    db = SessionLocal()

    # Read and encode uploaded image
    image = cv2.imread(image_path)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    uploaded_encodings = face_recognition.face_encodings(rgb_image)

    if not uploaded_encodings:
        print("❌ No face detected in uploaded image.")
        return "No face detected"

    uploaded_encoding = uploaded_encodings[0]

    # Fetch all students with stored face_data
    students = db.query(Student).filter(Student.face_data.isnot(None)).all()

    for student in students:
        try:
            stored_encoding = np.array(json.loads(student.face_data))
        except Exception as e:
            print(f"⚠️ Error decoding face data for {student.name}: {e}")
            continue

        match = face_recognition.compare_faces([stored_encoding], uploaded_encoding, tolerance=0.6)[0]
        if match:
            print(f"✅ Match found: {student.name}")
            db.close()
            return student.name

    db.close()
    print("❌ No matching face found.")
    return "Unknown"

