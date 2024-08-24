import face_recognition
import os

known_face_encodings = []
known_face_names = set()
# rtsp = "rtsp://admin:pass@123@192.168.1.240:554/cam/realmonitor?channel=2&subtype=0"
image_folder = 'image/politician'
def create_embedding():
    
    for filename in os.listdir(image_folder):
        if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.jpeg'):
            image_path = os.path.join(image_folder, filename)
            image = face_recognition.load_image_file(image_path)
            face_encodings = face_recognition.face_encodings(image)
            image_name= os.path.splitext(filename)[0]
            if face_encodings and image_name not in known_face_names:
                known_face_encodings.append(face_encodings[0])
                known_face_names.add(image_name)

    return known_face_encodings, known_face_names