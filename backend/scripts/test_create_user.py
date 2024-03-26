import requests

# Define the URL of the endpoint
url = 'http://127.0.0.1:5000/create_user'

# Define the data to be sent in the request body (in JSON format)
data = {
    'username': 'may2a',
    'password': 'maya123'
}

# Send a POST request to the endpoint
response = requests.post(url, json=data)

# Check the response status code
if response.status_code == 200:
    print("User created successfully")
else:
    print("Error:", response.text)
