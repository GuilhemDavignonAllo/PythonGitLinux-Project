import requests

def get_manor_ids(place_id):
    url = f"https://opendomesday.org/api/1.0/manor/{place_id}/"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    manors = data.get("manors")
    if manors is not None:
        return [manor["id"] for manor in manors]
    else:
        return []
if __name__ == '__main__':
    place_id = '20385'
    manor_ids = get_manor_ids(place_id)
    print(manor_ids)
