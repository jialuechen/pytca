from textblob import TextBlob
import pandas as pd

def analyze_sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity, analysis.sentiment.subjectivity

def sentiment_trend_over_time(texts):
    sentiment_data = []
    for timestamp, text in texts:
        polarity, _ = analyze_sentiment(text)
        sentiment_data.append({'timestamp': timestamp, 'sentiment': polarity})
    return pd.DataFrame(sentiment_data)
