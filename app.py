#!flask/bin/python
from flask import Flask, jsonify, request
from model import db, Location, User 
from flask_sqlalchemy import SQLAlchemy
from elevation import fetch_elevaion
from geopy import distance

from config import app_config


get_distances_form_query = lambda rows, location, dist = distance.distance: \
	tuple(map( dist, \
		map(lambda x: (
			x.latitude,\
			x.longitude,\
			*location
		), rows) \
	))

def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(app_config[config_name])
	
	db.init_app(app)

	@app.route('/location/<name>', methods=["PUT","GET"])
	def location_request(name):
		print (request.form)
		if request.method == 'PUT':
			lat = request.form["latitude"]
			lon = request.form["longitude"]

			db.session.add(Location(
				name = name,
				latitude = lat,
				longitude = lon,
				elevation  = fetch_elevaion( ( (lat, lon),) )[0],
			))

			db.session.commit()
			return jsonify(  { "message" : "success" } )

		if request.method == 'GET':
			r = db.Location.query().filter_by(name = name)
			return jsonify(r)

	@app.route('/closest', methods=["GET"])
	@app.route('/user/<user>/closest', methods=["GET"])
	def closest(user = None):
		lat = request.args.get("latitude")
		lon = request.args.get("longitude")
		r =  db.session.query(Location).all()

		distances = get_distances_form_query(r,(lat,lon))

		if not distances:
			return jsonify( {"closest": {}, }) 
		min_d = sorted(distances)[0]
		d = r[distances.index(min_d)]

		return jsonify({"closest": {
			"name": d["name"],
			"latitude": d["latitude"],
			"longitude": d["longitude"],
			"elevation": d["elevation"], 
		}})


	@app.route('/indistance', methods=["GET"])
	@app.route('/user/<user>/indistance', methods=["GET"])
	def indistance(user = None):
		r = db.session.query(Location).all()
		lat = request.args.get("latitude")
		lon = request.args.get("longitude")
		radius = request.args.get("radius")


		distances = get_distances_form_query(r, (lat,lon))
		f = sorted( filter( lambda x: x < radius, distances) )
		resp = []

		for x, n in zip(sorted(f), range(len(f))):
			d = r[distances.index(x)]
			resp.append({
				"name": d["name"],
				"latitude": d["latitude"],
				"longitude": d["longitude"],
				"elevation": d["elevation"], 
				"distance": x,
				"order": n
			})

		return jsonify({"indistance": resp, "radius": radius})
	
	return app
