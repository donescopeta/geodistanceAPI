from elevation import fetch_elevaion

def load_locations():
	for x in open("tests/example_locations.txt",'r').readlines():
		la,lo,nm = list([ y.strip() for y in x.split(',') ])
		yield float(la), float(lo),nm

def test_elevation_api():
	locations = load_locations()
	points = [ x[:2] for x in locations ]
	elevations = fetch_elevaion(points)
	# Dead Sea, Mount Everest
	assert \
		-440 < min(elevations) < -400 and \
		7900 < max(elevations) < 8700 
