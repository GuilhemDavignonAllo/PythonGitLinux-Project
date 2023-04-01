import requests

url = "https://opendomesday.org/api/places/?q=county:Derbyshire"
response = requests.get(url)
places = response.json()
place_ids = [place["id"] for place in places]
print(place_ids)
