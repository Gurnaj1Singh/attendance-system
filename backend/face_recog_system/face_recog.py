import face_recognition
import cv2
import os
import pickle

DATASET_PATH = "smart-hostel-attendance/backend/face_recog_system/dataset/"
ENCODINGS_FILE = "smart-hostel-attendance/backend/face_recog_system/encodings.pickle"

print(f"Checking dataset path: {os.path.abspath(DATASET_PATH)}")

def encode_faces():
    known_encodings = []
    known_names = []

    if not os.path.exists(DATASET_PATH):
        print("❌ Dataset folder not found! Create 'face_recog_system/dataset/' and add images.")
        return

    files_processed = 0
    faces_detected = 0

    for file in os.listdir(DATASET_PATH):
        if file.endswith(".jpg") or file.endswith(".png"):
            files_processed += 1
            image_path = os.path.join(DATASET_PATH, file)
            print(f"📷 Processing: {image_path}")

            image = cv2.imread(image_path)
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            face_locations = face_recognition.face_locations(rgb_image)
            face_encodings = face_recognition.face_encodings(rgb_image, face_locations)

            if face_encodings:
                faces_detected += 1
                known_encodings.append(face_encodings[0])
                known_names.append(file.split(".")[0])  # Use filename as student ID
                print(f"✅ Face detected in: {file}")
            else:
                print(f"⚠️ No face detected in: {file}")

    if files_processed == 0:
        print("❌ No images found! Add .jpg or .png files to 'dataset/'.")
        return

    if faces_detected == 0:
        print("❌ No faces detected in any image. Ensure clear front-facing images.")
        return

    # Save encodings
    with open(ENCODINGS_FILE, "wb") as f:
        pickle.dump({"encodings": known_encodings, "names": known_names}, f)

    print("🎉 Encoding process completed! Saved to 'encodings.pickle'.")

# Run the encoding function
encode_faces()

def recognize_face(image_path):
    import face_recognition
    import cv2
    import pickle
    import os

    ENCODINGS_FILE = "face_recog_system/encodings.pickle"

    # Ensure the encodings file exists
    if not os.path.exists(ENCODINGS_FILE):
        raise FileNotFoundError("❌ encodings.pickle file not found! Run face_recog.py to generate it.")

    # Load face encodings
    with open(ENCODINGS_FILE, "rb") as f:
        data = pickle.load(f)

    image = cv2.imread(image_path)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    face_locations = face_recognition.face_locations(rgb_image)
    face_encodings = face_recognition.face_encodings(rgb_image, face_locations)

    for encoding in face_encodings:
        matches = face_recognition.compare_faces(data["encodings"], encoding)
        name = "Unknown"

        if True in matches:
            matched_indexes = [i for i, match in enumerate(matches) if match]
            name = data["names"][matched_indexes[0]]

        return name  # Return the recognized student's name

    return "No face detected"

