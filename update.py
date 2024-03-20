import requests

# URL of the FastAPI endpoint for updating observations
url = "http://127.0.0.1:8000/observations/2"  # Replace '1' with the ID of the observation to update

# Updated data for the observation
updated_data = {
    "location": {"latitude": 40.712776, "longitude": -74.005974},
    "date_time": "2024-03-20T09:00:00Z",
    "description": "updated",
    "parameters": {
        "pH": 7.5,
        "conductivity": 260,
        "DO": 70,
        "contaminants": ["Lead", "Arsenic", "Copper"]
    }
}

# Sending a PUT request to update the observation with ID = 1
response = requests.put(url, json=updated_data)

# Checking the response
if response.status_code == 200:
    updated_observation = response.json()
    print("Observation updated successfully:")
    print(updated_observation)
else:
    print("Failed to update observation:", response.status_code)
    print("Response body:", response.json())
