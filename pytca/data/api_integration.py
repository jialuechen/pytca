import requests

def fetch_real_time_data(api_url, params):
    response = requests.get(api_url, params=params)
    return response.json()

def analyze_social_media_sentiment(api_url, params):
    response = requests.get(api_url, params=params)
    return response.json()
