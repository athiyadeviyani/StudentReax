from flask import Flask
import boto3
import json 

app = Flask(__name__)
@app.route("/")
def home():
    comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')
    text = "I hate my teacher"
    print(json.dumps(comprehend.detect_sentiment(Text=text, LanguageCode='en'), sort_keys=True, indent=4))
  #  return "Hello, World!"

if __name__ == "__main__":
    app.run(debug=True)


