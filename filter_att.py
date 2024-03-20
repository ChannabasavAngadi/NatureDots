import requests
from datetime import datetime

# URL of the FastAPI endpoint for filtering observations
url = "http://127.0.0.1:8000/observations/filter/"

# Define the start and end date for the date range
start_date = datetime(2024, 3, 19)
end_date = datetime(2024, 3, 20)

# Define other optional parameters (min_pH, max_pH, contaminants)
min_pH = 1
max_pH = 100
contaminants = "Lead"

# Sending a GET request to filter observations
response = requests.get(url, params={"start_date": start_date, "end_date": end_date, "min_pH": min_pH, "max_pH": max_pH, "contaminants": contaminants})

# Checking the response
if response.status_code == 200:
    filtered_observations = response.json()
    print("Filtered observations:")
    for observation in filtered_observations:
        print(observation)  # Print each observation
else:
    print("Failed to retrieve filtered observations:", response.status_code)
    print("Response body:", response.json())
