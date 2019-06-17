import requests
API = "https://elevation-api.io/api/elevation"
KEY = "n5iQbj-L4V-LfiZb4aZfuodM5fD5fA"

def fetch_elevaion(points):
	r = requests.get(
      	url=API,
		params = {
			"points": ",".join( [ "({0},{1})".format(*x) for x in points ] ),
			"key": KEY
		}
	)
	data = tuple([ x["elevation"] for x in r.json()["elevations"] ])
	return data
