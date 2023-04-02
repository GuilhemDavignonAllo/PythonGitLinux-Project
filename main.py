from manors import get_manor_ids
from manors import get_all_manor_info

df = get_all_manor_info()
print(df.head())

place_id = '20385'
manor_ids = get_manor_ids(place_id)
print(manor_ids)
