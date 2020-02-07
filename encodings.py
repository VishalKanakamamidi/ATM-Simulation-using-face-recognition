import face_recognition
import cv2
import numpy as np
from datetime import datetime
import os
k = os.listdir("known-people")
for i in k:
	image = face_recognition.load_image_file("known-people//"+i)
	face_encoding = face_recognition.face_encodings(image)[0]
	# print(len(face_encoding))
	# a = np.arange(face_encoding)
	np.save("Encodings//"+i[0:-4],face_encoding)
	# f.write(face_encoding)
	# f.close()