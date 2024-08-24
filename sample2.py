import os
from PIL import Image
import face_recognition

known_image_encodings=[]
known_faces= []
rootdir= "/home/soyasauce/Desktop/face_recognition/image"

for subdir, dirs,files in os.walk(rootdir):
    
    for image in files:

        img= os.path.join(subdir, image)
        
        person_id= image.split()[-1].replace('.jpg', '').replace('.jpeg', '').replace('.png', '')
        ##print(person_id)
        known_image_encodings.append(face_recognition.face_encodings(img)[0])
        known_faces.append(person_id)


