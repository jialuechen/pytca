import requests

url = 'http://localhost:5000/vwap'
data = {
    'prices': [100, 101, 102, 103, 104],
    'volumes': [10, 15, 10, 5, 20]
}
response = requests.post(url, json=data)
print(response.json())
