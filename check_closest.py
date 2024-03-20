import requests

# URL of the FastAPI endpoint for finding closest observations
url = "http://127.0.0.1:8000/observations/closest/"

# Coordinates for the location
latitude = 60.712776
longitude = -20.005974

# Sending a GET request to find closest observations
response = requests.get(url, params={"latitude": latitude, "longitude": longitude})

# Checking the response
if response.status_code == 200:
    closest_observations = response.json()
    print("Closest observations:")
    for observation in closest_observations:
        print(f"ID: {observation['id']}, Distance: {observation['distance']:.2f} km, Location: {observation['location']}")
else:
    print("Failed to retrieve closest observations:", response.status_code)
    print("Response body:", response.json())
