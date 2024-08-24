import face_recognition
import cv2
import os
import pandas as pd
from openpyxl import load_workbook
import datetime
import numpy as np

#Detected_Name = []
entry_set= set()

def append_to_excel(data, filename, sheet_name='Sheet1'):
    # Check if file exists
    try:
        # Try to open an existing workbook
        existing_data = pd.read_excel(filename, sheet_name=sheet_name)
        # convert unix time to local time
        ##data["Entry_Time"]= datetime.datetime.fromtimestamp(data["Entry_Time"])
        df = pd.DataFrame(data)
        #print("Before concat")
        # Append data to the existing data
        combined_data = pd.concat([existing_data, df], axis=0)
        #print("After concat")
        # Write to the file without duplicating the headers
        with pd.ExcelWriter(filename, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
            combined_data.to_excel(writer, sheet_name=sheet_name, index=False)

    except FileNotFoundError:
        # If the file doesn't exist, create a new one
        df = pd.DataFrame(data)
        df.to_excel(filename, sheet_name=sheet_name, index=False)


filename_excel = 'Attendance_Data.xlsx'
sheet_name = 'Sheet1'
initial_data = {'Name': [], 'Entry_Time': [], 'Exit_Time': []}
append_to_excel(initial_data, filename_excel, sheet_name)
known_face_encodings = []
known_face_names = []
# rtsp = "rtsp://admin:pass@123@192.168.1.240:554/cam/realmonitor?channel=2&subtype=0"
image_folder = 'image/politician'
for filename in os.listdir(image_folder):
    if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.jpeg'):
        image_path = os.path.join(image_folder, filename)
        image = face_recognition.load_image_file(image_path)
        face_encodings = face_recognition.face_encodings(image)
        if face_encodings:
            known_face_encodings.append(face_encodings[0])
            known_face_names.append(os.path.splitext(filename)[0])

#print(len(known_face_encodings))
#print(len(known_face_names))
for name in known_face_names:
    print(name)
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

    for index, ((top, right, bottom, left), face_encoding) in enumerate(zip(face_locations, face_encodings)):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"
        ##for element in matches:
        ##    print(element) return false if face_encoding do not match

        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding) 
        best_match_index = face_distances.argmin()
        #try:
        #    best_match_index=1
        #    print(1, best_match_index)
        #    best_match_index= np.where(face_distances==0)[0].item()
            
        #except ValueError:
        #    continue
        if best_match_index==0 and matches[index]==True:
            ##print(name)

            name = known_face_names[index]
            if name not in entry_set and name != 'Unknown':
                entry_set.add(name)
                print(f"Detected: {name}")
                #print("Detected")
                new_data = {
                    'Name': name,
                    'Entry_Time': [datetime.datetime.now()]
                }
            
                append_to_excel(new_data, filename_excel, sheet_name)
                #Detected_Name.append(name)

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        ## if time of the day 8pm then clear the detected students name
        if datetime.datetime.now().strftime('%H')=='20':
            entry_set.clear()
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
