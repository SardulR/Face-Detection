from flask import Flask, render_template, Response, redirect, url_for, jsonify, request
import cv2
import face_recognition

app = Flask(__name__)

# Load a sample image with a known face
Sardul_image = face_recognition.load_image_file("sardulr.jpg")
Sardul_encoding = face_recognition.face_encodings(Sardul_image)[0]

# Flag to check if the user is identified
user_identified = False

# Open the video camera (you can change the parameter to 0 for the default camera)
video_capture = cv2.VideoCapture(0)

def generate_frames():
    global user_identified  # Use the global variable

    while True:
        # Capture each frame from the video feed
        ret, frame = video_capture.read()

        # Find all face locations and face encodings in the current frame
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        user_identified = False  # Reset the flag for each frame

        for face_encoding in face_encodings:
            # Check if the face matches the known face
            matches = face_recognition.compare_faces([Sardul_encoding], face_encoding)

            if True in matches:
                user_identified = True
                break  # Break the loop if a match is found

        # Draw rectangles and names on the frame
        for (top, right, bottom, left) in face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Convert the frame to JPEG format
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Hardcoded user credentials for simplicity
valid_user = {
    "username": "Sardul",
    "password": "sardul12345",
}

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/validate_login', methods=['POST'])
def validate_login():
    username = request.form['username']
    password = request.form['password']

    if username == valid_user['username'] and password == valid_user['password']:
        # You can add session management or token generation here for a more secure solution
        return redirect(url_for('my_face_recognition'))
    else:
        return render_template('login.html', error='Invalid credentials')

@app.route('/my_face_recognition')
def my_face_recognition():
    return render_template('my_face_recognition.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/check_identification')
def check_identification():
    global user_identified  # Make sure to use the global variable

    return jsonify({'user_identified': user_identified})

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

if __name__ == '__main__':
    app.run(debug=True)
