import requests
import os
API = "https://elevation-api.io/api/elevation"
#KEY = "n5iQbj-L4V-LfiZb4aZfuodM5fD5fA"
KEY = os.getenv('ELEVATION_API_IO_KEY')

def fetch_elevaion(points):
	r = requests.get(
      	url=API,
		params = {
			"points": ",".join( [ "({0},{1})".format(*x) for x in points ] ),
			"key": KEY
		}
	)
	if r.status_code == 200:
		data = tuple([ x["elevation"] for x in r.json()["elevations"] ])
		return data
	else: return None
