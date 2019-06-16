import requests
API = "https://elevation-api.io/api/elevation"
KEY = "n5iQbj-L4V-LfiZb4aZfuodM5fD5fA"

def fetch_elevaion(points):
	r = requests.get(
      	API,
		params = {
			"points": str( tuple( [ tuple(p) for p in points ] ) ),
			"key": KEY
		}
	)
	return tuple([ x["elevation"] for x  in r ])
