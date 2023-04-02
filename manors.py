import requests
import pandas as pd
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



def get_derbyshire_places():
    response = requests.get("https://opendomesday.org/api/1.0/manor/?county=Derbyshire")
    response.raise_for_status()
    data = response.json()
    return data["places"]

def get_all_manor_ids():
    derbyshire_places = get_derbyshire_places()
    manor_ids = []
    for place in derbyshire_places:
        manor_ids += get_manor_ids(place["id"])
    return manor_ids

def get_manor_info(manor_id):
    url = f"https://opendomesday.org/api/1.0/manor/{manor_id}/"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    geld_paid = data["geld_paid"]
    total_ploughs = data["total_ploughs"]
    return {
        "id": manor_id,
        "name": data["name"],
        "place_id": data["place"]["id"],
        "place_name": data["place"]["name"],
        "geld_paid": geld_paid,
        "total_ploughs": total_ploughs
    }

def get_all_manor_info():

    """
    Retrieve the geld paid and total ploughs owned for all manors in Derbyshire and return a Pandas DataFrame.

    Returns:
        pandas.DataFrame: A DataFrame containing the geld paid and total ploughs owned for each manor.
    """
    manor_ids = get_all_manor_ids()
    manor_info = []
    for manor_id in manor_ids:
        manor_info.append(get_manor_info(manor_id))
    return pd.DataFrame(manor_info)


if __name__ == '__main__':
    
    manor_df = get_all_manor_info()
    geld_paid_sum = manor_df["geld_paid"].sum()
    total_ploughs_sum = manor_df["total_ploughs"].sum()
    place_id = '20385'
    manor_ids = get_manor_ids(place_id)
    print(manor_ids)
