import requests


product_id = input("what is the produc id you want ot use?\n")

try:
  product_id = int(product_id)
except:
  product_id = None
  print(f'{product_id} not valid id')

if product_id:

  endpoint = f"http://localhost:8000/api/products/{product_id}/delete/" #http://127.0.0.1:8000/  
  get_response = requests.delete(endpoint) # HTTP Request

  print(get_response.status_code, get_response.status_code == 204)