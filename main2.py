import face_recognition
import cv2
import os
import pandas as pd
from openpyxl import load_workbook
import datetime
from process_excel import append_to_excel, add_data, show_data, create_database

##Detected_Name = []
Entry_set= set()

##Exit_time= '22'


'''
def append_to_excel(data, filename, sheet_name='Sheet1', entry=0):
    # Check if file exists
    try:
        # Try to open an existing workbook
        existing_data = pd.read_excel(filename, sheet_name=sheet_name)
        

        # Append data to the existing data
        if entry==0:
            df = pd.DataFrame(data)
            combined_data = pd.concat([existing_data, df])
            with pd.ExcelWriter(filename, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
                combined_data.to_excel(writer, sheet_name=sheet_name, index=False)

        # this is to exit time 
        elif entry==1:
            existing_data.loc[existing_data['Name']==data['Name'], 'Exit_Time']= [data['Exit_time']]
            with pd.ExcelWriter(filename, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
                existing_data.to_excel(writer, sheet_name=sheet_name, index=False)
            

    except FileNotFoundError:
        # If the file doesn't exist, create a new one
        df = pd.DataFrame(data)
        df.to_excel(filename, sheet_name=sheet_name, index=False)
'''

#filename_excel = 'Attendance_Data.xlsx'
#sheet_name = 'Sheet1'
#initial_data = {'Name': [], 'Entry_Time': [], 'Exit_Time': []}
#append_to_excel(initial_data, filename_excel, sheet_name)
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

def prepare_data(name, time):
    
    if time.strftime('%H')<'20':
        print(f"Detected: {name}")
        new_data = {
            'Name': name,
            'Entry_Time': time
        }
        
        ##append_to_excel(new_data, filename_excel, sheet_name, 0)
        add_data(new_data)
    '''
    elif time.strftime('%H')>= Exit_time:
        new_data= {
            'Name': name,
            'Exit_time': time
        }
        append_to_excel(new_data, filename_excel, sheet_name, 1)
    '''
    

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

while True:
    ret, frame = cap.read()

    if not ret:
        print("Error: Could not read frame.")
        break
    # create database imported from process_excel
    create_database()

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
            if name not in Entry_set and name != 'Unknown' and datetime.datetime.now().strftime('%H')<Exit_time:
                time= datetime.datetime.now()                
                
                Entry_set.add(name)
                prepare_data(name, time)
            
            '''
            if name in Entry_set and datetime.datetime.now().strftime('%H')>= Exit_time:
                time= datetime.datetime.now()
                Entry_set.remove(name)
                prepare_data(name, time)
            '''
            

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        
        # this will clear the set data-structure when time is 8pm
        if datetime.datetime.now().strftime('%H')=='20':
            append_to_excel()
            Entry_set.clear()
            os.remove('database.db')

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
