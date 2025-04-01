import requests
import json

# Define the URL of the FastAPI endpoint
url = "http://python_api:8000/predict"

# Example payload to send to the API
payload = {
    "data": [
        [1, "item_1", "d_1"],
        [2, "item_2", "d_2"]
    ],
    "columns": ["data", "item_id", "d"]
}

# Send a POST request to the API
response = requests.post(url, json=payload)

# Print the response
if response.status_code == 200:
    print("Response from API:")
    print(json.dumps(response.json(), indent=4))
else:
    print(f"Error: {response.status_code}")
    print(response.text)