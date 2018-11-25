from Tkinter import *
import tkMessageBox as messagebox
import boto3
import json 
import csv
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import tkFileDialog as fd
import os
import PIL.Image 
import PIL.ImageTk
import numpy  # Import numpy
from drawnow import *
import datetime
import cv2
import time
import face_recognition

window = Tk()
window.title("Student | REAX")

window.geometry('300x400')

spc = Label(window, text = "", font = ("Arial Bold",20))
spc.pack()

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

image = PIL.Image.open(resource_path("logo.png")).resize((200, 200), PIL.Image.ANTIALIAS)
photo = PIL.ImageTk.PhotoImage(image)

label = Label(image=photo)
label.image = photo # keep a reference!
label.pack()

def create_report():
    inf2a = []
    inf2ccs = []
    inf2cse = []
    dmmr = []

    #with open('feedback.csv') as csv_file:
    with open('feedback.csv') as csv_file:
        
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0

        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                if (row[1] == 'INF2A'):
                    inf2a.append(row[2])
                elif (row[1] == 'INF2C-CS'):
                    inf2ccs.append(row[2])
                elif (row[1] == 'INF2C-SE'):
                    inf2cse.append(row[2])
                elif (row[1] == 'DMMR'):
                    dmmr.append(row[2])

        course_arrays = [inf2a, inf2ccs, inf2cse, dmmr]

        for course in course_arrays:
            mixedcount = 0
            positivecount = 0
            negativecount = 0
            neutralcount = 0
            total = 0
            for feedback in course:
                total += 1
                comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')
                result = json.dumps(comprehend.detect_sentiment(Text=feedback, LanguageCode='en'), sort_keys=True, indent=4)
                stuff = json.loads(result)

                for k in stuff.items():
                    if 'Sentiment' in k:
                        result = k[1].lower()
                        if (result == "positive"):
                            positivecount += 1
                        if (result == "negative"):
                            negativecount += 1
                        if (result == "neutral"):
                            neutralcount += 1
                        if (result == "mixed"):
                            mixedcount += 1

    # for course in course_arrays:
    
            # Data to plot
            title = ""
            if course == inf2a:
                title = "INF2A"
            elif course == inf2ccs:
                title = "INF2C-CS"
            elif course == inf2cse:
                title = "INF2C-SE"
            elif course == dmmr:
                title = "DMMR"

            plt.title(title)
            labels = 'Positive', 'Negative', 'Mixed', 'Neutral'
            sizes = [positivecount * 100/ total, negativecount * 100/ total, mixedcount * 100/ total, neutralcount * 100/ total]
            colors = ['yellowgreen', 'lightcoral', 'lightskyblue', 'gold']
            plt.pie(sizes)
            patches, texts = plt.pie(sizes, colors=colors, startangle=90)
            plt.legend(patches, labels, loc="best")
            plt.axis('equal')
            plt.tight_layout()
            #plt.show()
            plt.savefig(title + '_report.png')
    

    
    messagebox.showinfo('MESSAGE', 'Reports are successfully generated!')
    exit()

def view_statistics():
    inf2a = []
    inf2ccs = []
    inf2cse = []
    dmmr = []

    #with open('feedback.csv') as csv_file:
    with open('feedback.csv') as csv_file:
        
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0

        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                line_count += 1
                if (row[1] == 'INF2A'):
                    inf2a.append(row[2])
                elif (row[1] == 'INF2C-CS'):
                    inf2ccs.append(row[2])
                elif (row[1] == 'INF2C-SE'):
                    inf2cse.append(row[2])
                elif (row[1] == 'DMMR'):
                    dmmr.append(row[2])

        course_arrays = [inf2a, inf2ccs, inf2cse, dmmr]
        f = open('output.txt','w')

        print >> f, "Course Feedback Statistics for INFORMATICS 2018/19"
        print >> f, ""
        print >> f, "#######################################"

        for course in course_arrays:
            mixedcount = 0
            positivecount = 0
            negativecount = 0
            neutralcount = 0
            total = 0
            for feedback in course:
                total += 1
                comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')
                result = json.dumps(comprehend.detect_sentiment(Text=feedback, LanguageCode='en'), sort_keys=True, indent=4)
                stuff = json.loads(result)

                for k in stuff.items():
                    if 'Sentiment' in k:
                        result = k[1].lower()
                        if (result == "positive"):
                            positivecount += 1
                        if (result == "negative"):
                            negativecount += 1
                        if (result == "neutral"):
                            neutralcount += 1
                        if (result == "mixed"):
                            mixedcount += 1

            #print("COURSE NAME: " + row[1])
            print >>f, ""
            if course == inf2a:
                print >>f, "COURSE NAME: INF2A"
            elif course == inf2ccs:
                print >>f, "COURSE NAME: INF2C-CS"
            elif course == inf2cse:
                print >>f, "COURSE NAME: INF2C-SE"
            elif course == dmmr:
                print >>f, "COURSE NAME: DMMR"

            print >>f, "POSITIVE: " + "%.2f" % (positivecount * 100/ total) + "% " + str(positivecount) + "/" + str(total)
            print >>f, "NEGATIVE: " + "%.2f" % (negativecount * 100/ total) + "%" + str(negativecount) + "/" + str(total)
            print >>f, "MIXED: " + "%.2f" % (mixedcount * 100/ total) + "%" + str(mixedcount) + "/" + str(total)
            print >>f, "NEUTRAL: " + "%.2f" % (neutralcount * 100/ total) + "%" + str(neutralcount) + "/" + str(total)
            print >>f, ""
            print >>f, "#######################################"

    print >> f, ""
    print >> f, "Total number of feedback received = " + str(line_count - 1)
    messagebox.showinfo('MESSAGE', 'Complete statistics are successfully printed to output.txt!')

BUCKET = "com-oxfordhack-enable"
KEY = "ouput.txt"
IMAGE_ID = KEY
FEATURES_BLACKLIST = ("Landmarks", "Emotions", "Pose", "Quality", "BoundingBox", "Confidence")
COLLECTION = "my-collection-id"

s3 = boto3.client('s3')
file_name = '/Users/Edon/Desktop/oxhack-master/output.txt'
key_name = 'output.txt'
s3.upload_file(file_name, BUCKET, key_name)


def view_all():
    os.system("open " + str(resource_path("feedback.csv")))

def facedet():
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
            calmness.append(averageCalm / count)
            happiness.append(averageHappy / count)

            for face in detect_faces(BUCKET, KEY):
                maxpercent = 0
                print "Face ({Confidence}%)".format(**face)
                for emotion in face['Emotions']:
                    print"  {Type} : {Confidence}%".format(**emotion)
                    if maxpercent < emotion['Confidence']:
                        maxpercent = emotion['Confidence']
                        emotionType = emotion['Type']
                    # print"  {Type} : {Confidence}%".format(**emotion)
                known_face_names.append(emotionType)
                print(emotionType)

            startTime = datetime.datetime.now()
        # Grab a single frame of video
        drawnow(makeFig)  # Call drawnow to update our live graph
        plt.pause(.000001)  # Pause Briefly. Important to keep drawnow from crashing
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
            exit()

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()



lbl = Label(window, text = "", font = ("Arial Bold",20))
lbl.pack()

btn1 = Button(window, text = "Generate Report", command = create_report, font = 30)
btn1.pack()

btn2 = Button(window, text = "View Statistics", command = view_statistics, font = 30)
btn2.pack()

btn3 = Button(window, text = "Full Feedback List", command = view_all, font = 30)
btn3.pack()

btn4 = Button(window, text = "View live graph", command = facedet, font = 30)
btn4.pack()


window.mainloop()
