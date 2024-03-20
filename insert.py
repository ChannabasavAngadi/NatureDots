import requests

url = "http://127.0.0.1:8000/observations/"

# Example data for creating a new observation
data = {
    "location": {"latitude": 40.712776, "longitude": -74.005974},
    "date_time": "2024-03-19T15:00:00Z",
    "description": "early afternoon water quality observation at Nehru Park",
    "parameters": {
        "pH": 7.4,
        "conductivity": 250,
        "DO": 67,
        "contaminants": ["Lead", "Arsenic"]
    }
}

response = requests.post(url, json=data)

print("Response:", response.status_code)
print("Response Body:", response.json())
