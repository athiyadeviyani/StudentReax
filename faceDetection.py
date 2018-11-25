import boto3
import datetime
import os
import cv2
import time
import face_recognition
import numpy  # Import numpy
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt  # import matplotlib library
from drawnow import *

startTime = datetime.datetime.now()

BUCKET = "com-oxfordhack-enable"
KEY = "test5.jpg"
IMAGE_ID = KEY
FEATURES_BLACKLIST = ("Landmarks", "Emotions", "Pose", "Quality", "BoundingBox", "Confidence")
COLLECTION = "my-collection-id"

s3 = boto3.client('s3')
file_name = '/Users/Edon/Desktop/test5.jpg'
key_name = 'test5.jpg'


def detect_faces(bucket, key, attributes=['ALL'], region="us-east-1"):
	rekognition = boto3.client("rekognition", region)
	response = rekognition.detect_faces(
		Image={
			"S3Object": {
				"Bucket": bucket,
				"Name": key,
			}
		},
		Attributes=attributes,
	)
	return response['FaceDetails']

def index_faces(bucket, key, collection_id, image_id=None, attributes=(), region="us-east-1"):
	rekognition = boto3.client("rekognition", region)
	response = rekognition.index_faces(
		Image={
			"S3Object": {
				"Bucket": bucket,
				"Name": key,
			}
		},
		CollectionId=collection_id,
		ExternalImageId=image_id,
		DetectionAttributes=attributes,
	)
	return response['FaceRecords']

video_capture = cv2.VideoCapture(0)


# Initialize some variables
face_locations = []
face_location = []
face_encodings = []
face_names = []
known_face_names = []
known_face_encodings = []
process_this_frame = True
emotionType = ""

while True:
    maxpercent = 0
    ret, frame = video_capture.read()

    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]
    # Only process every other frame of video to save time

    if (datetime.datetime.now() - startTime).total_seconds() >= 10:
        known_face_encodings = []
        known_face_names = []
        cv2.imwrite('/Users/Edon/Desktop/test5.jpg', frame)
        s3.upload_file(file_name, BUCKET, key_name)
        face_location = face_recognition.face_locations(rgb_small_frame)
        known_face_encodings = (face_recognition.face_encodings(rgb_small_frame, face_locations))

        for face in detect_faces(BUCKET, KEY):
            maxpercent = 0
            print "Face ({Confidence}%)".format(**face)
            for emotion in face['Emotions']:
                print"  {Type} : {Confidence}%".format(**emotion)
                if maxpercent < emotion['Confidence']:
                    maxpercent = emotion['Confidence']
                    emotionType = emotion['Type']
                #print"  {Type} : {Confidence}%".format(**emotion)
            known_face_names.append(emotionType)
            print(emotionType)

        startTime = datetime.datetime.now()
    # Grab a single frame of video

    # Resize frame of video to 1/4 size for faster face recognition processing

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, 0.55)
            name = ""
            # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
            # See if the face is a match for the known face(s)
            # If a match was found in known_face_encodings, just use the first one.
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
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
