import requests

# URL of the FastAPI endpoint for deleting observations
url = "http://127.0.0.1:8000/observations/1"  # Replace '1' with the ID of the observation to delete

# Sending a DELETE request to delete the observation with ID = 1
response = requests.delete(url)

# Checking the response
if response.status_code == 200:
    print("Observation deleted successfully")
else:
    try:
        # Try to decode the response content as JSON
        error_message = response.json()
        print("Failed to delete observation:", error_message)
    except Exception as e:
        # If decoding as JSON fails, print the raw response content
        print("Failed to delete observation. Error:", e)
        print("Response content:", response.content)
