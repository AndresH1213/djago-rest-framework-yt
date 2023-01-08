import requests

endpoint = "http://localhost:8000/api/products/" #http://127.0.0.1:8000/ 

data = {
  "title": "This field is done",
  "price": 32.99
}

get_response = requests.post(endpoint, json=data) # HTTP Request

print(get_response.json())
# print(get_response.status_code)