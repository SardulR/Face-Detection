import cv2
import face_recognition

# Load a sample image with a known face
Sardul_image = face_recognition.load_image_file("sardulr.jpg")
Sardul_encoding = face_recognition.face_encodings(Sardul_image)[0]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []

# Open the video camera (you can change the parameter to 0 for the default camera)
video_capture = cv2.VideoCapture(0)

while True:
    # Capture each frame from the video feed
    ret, frame = video_capture.read()

    # Find all face locations and face encodings in the current frame
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    face_names = []
    for face_encoding in face_encodings:
        # Check if the face matches the known face
        matches = face_recognition.compare_faces([Sardul_encoding], face_encoding)
        name = "Unknown"

        if True in matches:
            name = "Sardul R"

        face_names.append(name)

    # Draw rectangles and names on the frame
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

    # Display the resulting frame
    cv2.imshow('Video', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object
video_capture.release()

# Destroy all OpenCV windows
cv2.destroyAllWindows()
