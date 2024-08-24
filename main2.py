import face_recognition
import cv2
import os
import pandas as pd
import datetime
from process_excel import append_to_excel, add_data, show_data, create_database, reset_db
from image_embedding import create_embedding
##Detected_Name = []
Entry_set= set()

known_face_encodings, known_face_names= create_embedding()
create_database()
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

while True:
    ret, frame = cap.read()

    if not ret:
        print("Error: Could not read frame.")
        break
    

    frame= cv2.flip(frame, 1)
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = face_distances.argmin()
        if matches[best_match_index]:
            #print(name)
            name = known_face_names[best_match_index]
            if name not in Entry_set and name != 'Unknown':
                time= datetime.datetime.now().strftime("%H-%M-%S")               
                
                Entry_set.add(name)
                print(f"Detected: {name}")
                new_data = {
                    'Name': name,
                    'Entry_Time': time
                }
                add_data(new_data)
            

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        
        # this will clear the set data-structure when time is 8pm
        if datetime.datetime.now().strftime('%H')=='20':
            append_to_excel()
            Entry_set.clear()
            reset_db()

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()