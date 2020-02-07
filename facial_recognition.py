import face_recognition
import cv2
import numpy as np
from datetime import datetime
import os

Acc_name = "Vishal"
video_capture = cv2.VideoCapture(0) #"rtmp://192.168.43.21:1935/live/stream.flv"

# Load a sample picture and learn how to recognize it.



# rishav_image = face_recognition.load_image_file("known-people//rishav.jpg")
# rishav_face_encoding = face_recognition.face_encodings(rishav_image)[0]


# # Load a second sample picture and learn how to recognize it.
# vishal_image = face_recognition.load_image_file("known-people//vishal.jpg")
# vishal_face_encoding = face_recognition.face_encodings(vishal_image)[0]


# anuj_image = face_recognition.load_image_file("known-people//anuj.jpg")
# anuj_face_encoding = face_recognition.face_encodings(anuj_image)[0]

# mubaris_image = face_recognition.load_image_file("known-people//mubaris.jpg")
# mubaris_face_encoding = face_recognition.face_encodings(mubaris_image)[0]
known_face_encodings = list()
known_face_names = list()

k = os.listdir("Encodings")
check_Acc = 0
for i in k:
    b = np.load("Encodings//"+i)
    known_face_encodings.append(b)
    known_face_names.append(i[0:-4])




# Create arrays of known face encodings and their names
# known_face_encodings = [
#     rishav_face_encoding,
#     vishal_face_encoding,
#     anuj_face_encoding,
#     mubaris_face_encoding

# ]
# known_face_names = [
#     "rishav",
#     "vishal",
#     "anuj",
#     "mubaris"
# ]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
num = len(known_face_names)
list_names = [0]*num 
c = 1
listy = list()


while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                now = datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                dt_string1 = now.strftime("%d/%m/%Y")
                k = dt_string.split(":")
                k = int(k[-1])
                
                 
                if(k%3 == 0 and c == 1):
                    max1 = max(list_names)
                    n1 = list_names.index(max1)
                    if(max1 >= 12):
                        listy.append(known_face_names[n1]+" "+dt_string1)
                        print(known_face_names[n1]," ",dt_string)
                        check_Acc = check_Acc+1

                    list_names = [0]*num 
                    c = 0
                    continue
                if(k%3 != 0):
                    for i in range(0,num):
                        if (name == known_face_names[i]):
                            list_names[i] = list_names[i]+1
                            c = 1
                            continue
                else:
                    for i in range(0,num):
                        if (name == known_face_names[i]):
                            list_names[i] = list_names[i]+1
                            continue





            # if name == "Unknown" :
            #     name1 = input("Enter your name -- ")
            #     cv2.imwrite("known-people/"+name1+".jpg",small_frame)
                
            face_names.append(name)

    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if(check_Acc == 2):
        break
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
