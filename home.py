import boto3
import json 

comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')
text = "ILA is such a shitty course. Fuck that Pamela bitch"
result = json.dumps(comprehend.detect_sentiment(Text=text, LanguageCode='en'), sort_keys=True, indent=4)
stuff = json.loads(result)

print(stuff)

result = ""
for k in stuff.items():
    if 'Sentiment' in k:
        result = k[1].lower()
        print(k[1])

for j in stuff.items():
    if 'SentimentScore' in j:
        for i in (j[1]).keys():
            if result.lower() in i.lower():
                percentage = j[1][i] * 100    
                print("%.2f" % percentage + "%")
