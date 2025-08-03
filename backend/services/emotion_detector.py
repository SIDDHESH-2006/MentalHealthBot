from transformers import pipeline
from textblob import TextBlob

classifier = pipeline("text-classification", model="bhadresh-savani/distilbert-base-uncased-emotion")

def analyze_emotion(text: str):
    emotion_pred = classifier(text)[0]
    polarity = TextBlob(text).sentiment.polarity
    return emotion_pred["label"], round(polarity, 2)
