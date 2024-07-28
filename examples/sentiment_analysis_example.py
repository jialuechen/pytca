from pytca.analysis.sentiment.sentiment_analysis import analyze_sentiment, sentiment_trend_over_time
import pandas as pd

# Example text data for sentiment analysis
texts = [
    "The market is booming! Great time to invest.",
    "Stocks are plummeting due to economic uncertainty.",
    "Mixed signals from the market; experts are divided.",
    "Tech stocks are rising, but overall market sentiment is cautious.",
    "Unexpected gains in the market today, driving positive sentiment."
]

# Analyzing individual sentiments
for i, text in enumerate(texts):
    polarity, subjectivity = analyze_sentiment(text)
    print(f"Text {i+1}: Polarity={polarity}, Subjectivity={subjectivity}")

# Example data with timestamps for sentiment trend analysis
text_data = [
    ("2024-01-01 08:00:00", "The market is booming! Great time to invest."),
    ("2024-01-02 08:00:00", "Stocks are plummeting due to economic uncertainty."),
    ("2024-01-03 08:00:00", "Mixed signals from the market; experts are divided."),
    ("2024-01-04 08:00:00", "Tech stocks are rising, but overall market sentiment is cautious."),
    ("2024-01-05 08:00:00", "Unexpected gains in the market today, driving positive sentiment.")
]

# Convert the data to a DataFrame for easier manipulation
df = pd.DataFrame(text_data, columns=['timestamp', 'text'])

# Analyze sentiment trend over time
sentiment_trends = sentiment_trend_over_time(df.values)

# Display sentiment trend data
print("Sentiment Trends Over Time:")
print(sentiment_trends)
