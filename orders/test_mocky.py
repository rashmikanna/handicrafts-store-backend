import requests

url = "https://run.mocky.io/v3/81cefc93-7dd3-4c8d-b7ae-22f1aa0d144e"
response = requests.post(url)

print("Status Code:", response.status_code)
print("Response Text:", response.text)
