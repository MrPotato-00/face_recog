import face_recognition
import cv2 as cv
from sample2 import known_face_encodings

cam= cv.VideoCapture(0)

while True:
    _, img= cam.read()

    face_locations= face_recognition.face_locations(img)
    face_encodings= face_recognition.face_encodings(face_locations, face_locations)

    for (top,bottom, left,right) ,face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
