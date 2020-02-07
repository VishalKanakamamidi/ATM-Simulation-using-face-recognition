from flask import Flask, jsonify, render_template
from flask.views import MethodView
from flask_simplelogin import SimpleLogin, get_username, login_required
import os
import face_recognition
import cv2
import numpy as np
from datetime import datetime


my_users = {
    'Teacher': {'password': 'teacher', 'roles': ['admin']},
    'Vishal': {'password': 'vishal', 'roles': []},
    'mary': {'password': 'jane', 'roles': []},
    'anuj': {'password': '1234', 'roles': []},
   
}


def check_my_users(user):
    """Check if user exists and its credentials.
    Take a look at encrypt_app.py and encrypt_cli.py
     to see how to encrypt passwords
    """
    user_data = my_users.get(user['username'])
    if not user_data:
        return False  # <--- invalid credentials
    elif user_data.get('password') == user['password']:
        return True  # <--- user is logged in!

    return False  # <--- invalid credentials

PEOPLE_FOLDER = os.path.join('static', 'people_photo')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER
app.config['SECRET_KEY'] = 'secret-here'


SimpleLogin(app, login_checker=check_my_users)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/secret')
@login_required(username=['Vishal', 'anuj'])
def secret():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'Account-info.png')
    Acc_name = get_username()
    print(Acc_name)
    video_capture = cv2.VideoCapture(0)
    known_face_encodings = list()
    known_face_names = list()

    k = os.listdir("Encodings")
    check_Acc = 0
    for i in k:
        b = np.load("Encodings//"+i)
        known_face_encodings.append(b)
        known_face_names.append(i[0:-4])





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
        window_name = "Video"
        cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow(window_name, frame)
        cv2.imwrite("frames.jpg",frame)

        # Hit 'q' on the keyboard to quit!
        if(check_Acc == 2):
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()
    if(check_Acc == 2):
        return render_template('secret.html', user_image = full_filename)

    


@app.route('/api', methods=['POST'])
@login_required(basic=True)
def api():
    return jsonify(data='You are logged in with basic auth')


def be_admin(username):
    """Validator to check if user has admin role"""
    user_data = my_users.get(username)
    if not user_data or 'admin' not in user_data.get('roles', []):
        return "User does not have admin role"


def have_approval(username):
    """Validator: all users approved, return None"""
    return


@app.route('/complex')
@login_required(must=[be_admin, have_approval])
def complexview():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'vishal.jpg')
    return render_template('secret1.html', user_image = full_filename)


class ProtectedView(MethodView):
    decorators = [login_required]

    def get(self):
        return "You are logged in as <b>{0}</b>".format(get_username())


app.add_url_rule('/protected', view_func=ProtectedView.as_view('protected'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, use_reloader=True, debug=True)
