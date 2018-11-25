from tkinter import *
from tkinter import messagebox
import boto3
import json 
import csv
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from tkinter import filedialog as fd
import os
import PIL.Image 
import PIL.ImageTk

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
            print("",file=f)
            if course == inf2a:
                print("COURSE NAME: INF2A",file=f)
            elif course == inf2ccs:
                print("COURSE NAME: INF2C-CS", file=f)
            elif course == inf2cse:
                print("COURSE NAME: INF2C-SE", file=f)
            elif course == dmmr:
                print("COURSE NAME: DMMR", file=f)

            print("POSITIVE: " + "%.2f" % (positivecount * 100/ total) + "%", file=f)
            print("NEGATIVE: " + "%.2f" % (negativecount * 100/ total) + "%", file=f)
            print("MIXED: " + "%.2f" % (mixedcount * 100/ total) + "%", file=f)
            print("NEUTRAL: " + "%.2f" % (neutralcount * 100/ total) + "%", file=f)
            print("",file=f)
            print("#######################################",file=f)
            print("",file=f)
    
    messagebox.showinfo('MESSAGE', 'Complete statistics are successfully printed to output.txt!')
    exit()

def view_all():
    os.system("open " + str(resource_path("feedback.csv")))

lbl = Label(window, text = "", font = ("Arial Bold",20))
lbl.pack()

btn1 = Button(window, text = "Generate Report", command = create_report, font = 30)
btn1.pack()

btn2 = Button(window, text = "View Statistics", command = view_statistics, font = 30)
btn2.pack()

btn3 = Button(window, text = "Full Feedback List", command = view_all, font = 30)
btn3.pack()


window.mainloop()



