import boto3
import json 
import tkinter as tk
from tkinter.filedialog import askopenfilename
import csv
#import pandas as pd

inf2a = []
inf2ccs = []
inf2cse = []
dmmr = []

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

        #print("COURSE NAME: " + row[1])
        print("")
        if course == inf2a:
            print("COURSE NAME: INF2A")
        elif course == inf2ccs:
            print("COURSE NAME: INF2C-CS")
        elif course == inf2cse:
            print("COURSE NAME: INF2C-SE")
        elif course == dmmr:
            print("COURSE NAME: DMMR")

        print("POSITIVE: " + "%.2f" % (positivecount * 100/ total) + "%")
        print("NEGATIVE: " + "%.2f" % (negativecount * 100/ total) + "%")
        print("MIXED: " + "%.2f" % (mixedcount * 100/ total) + "%")
        print("NEUTRAL: " + "%.2f" % (neutralcount * 100/ total) + "%")
        print("")
        print("#######################################")
        print("")

        import matplotlib.pyplot as plt
 
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
        patches, texts = plt.pie(sizes, colors=colors, shadow=True, startangle=90)
        plt.legend(patches, labels, loc="best")
        plt.axis('equal')
        plt.tight_layout()
        plt.show()




        #if row > 0:
            #text = (row[2])

#            comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')
            #text = "I am not sure about my feelings towards Calculus."
 #           result = json.dumps(comprehend.detect_sentiment(Text=text, LanguageCode='en'), sort_keys=True, indent=4)
  #          stuff = json.loads(result)

           # print(stuff)

    #        result = ""
   #         for k in stuff.items():
     #           if 'Sentiment' in k:
      #              result = k[1].lower()
       #             print(k[1])

        #    for j in stuff.items():
         #       if 'SentimentScore' in j:
          #          for i in (j[1]).keys():
           #             if result.lower() in i.lower():
            #                percentage = j[1][i] * 100    
             #               print("%.2f" % percentage + "%")

