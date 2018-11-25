import numpy  # Import numpy
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt  # import matplotlib library
from drawnow import *
import boto3
import datetime
import os
import cv2
import time

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


happiness = []
calmness = []
plt.ion()  # Tell matplotlib you want interactive mode to plot live data


def makeFig():  # Create a function that makes our desired plot
    plt.ylim(0, 100)  # Set y min and max values
    plt.title('Happiness and Calmness against time')  # Plot the title
    plt.grid(True)  # Turn the grid on
    plt.ylabel('Percentage')  # Set ylabels
    plt.plot(happiness, 'ro-', label='Happiness')
    plt.legend(loc='upper right')  # plot the legend
    plt.plot(calmness, 'b^-', label='Calmness')
    plt.ticklabel_format(useOffset=False)  # Force matplotlib to NOT autoscale y axis
    plt.legend(loc='upper left')  # plot the legend


def update():
    cap = cv2.VideoCapture(0)
    time.sleep(3)
    ret, frame = cap.read()
    cv2.imwrite('/Users/Edon/Desktop/test5.jpg', frame)
    s3.upload_file(file_name, BUCKET, key_name)
    averageCalm = 0
    averageHappy = 0
    count = 0
    for face in detect_faces(BUCKET, KEY):
        count += 1
        print "Face ({Confidence}%)".format(**face)
        for emotion in face['Emotions']:
            if emotion['Type'] == 'CALM':
                averageCalm += emotion['Confidence']
            elif emotion['Type'] == 'HAPPY':
                averageHappy += emotion['Confidence']
            print"  {Type} : {Confidence}%".format(**emotion)
    calmness.append(averageCalm/count)
    happiness.append(averageHappy/count)


while True:  # While loop that loops forever

    if (datetime.datetime.now() - startTime).total_seconds() >= 5:
        update()
        startTime = datetime.datetime.now()

    drawnow(makeFig)  # Call drawnow to update our live graph
    plt.pause(.000001)  # Pause Briefly. Important to keep drawnow from crashing
