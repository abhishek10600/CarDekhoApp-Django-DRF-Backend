import requests

endpoint = "http://127.0.0.1:8000/car/list"

get_response = requests.get(endpoint)

print(get_response.json())
print(get_response.status_code)
