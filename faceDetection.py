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

while True:
    if (datetime.datetime.now() - startTime).total_seconds() >= 5:
        cap = cv2.VideoCapture(0)
        time.sleep(3)
        ret, frame = cap.read()
        cv2.imwrite('/Users/Edon/Desktop/test5.jpg', frame)
        s3.upload_file(file_name, BUCKET, key_name)
        for face in detect_faces(BUCKET, KEY):
            print "Face ({Confidence}%)".format(**face)
            for emotion in face['Emotions']:
                print"  {Type} : {Confidence}%".format(**emotion)

        startTime = datetime.datetime.now()
