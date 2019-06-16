#!flask/bin/python
from flask import Flask, jsonify, request
from model import db, Location, User 
from flask_sqlalchemy import SQLAlchemy
from elevation import fetch_elevaion
from geopy import distance

from config import app_config


getdistances = lambda r, t: tuple(map( \
	distance.distance,\
	map(lambda x: ((x.latitude, x.longitude), t ) ) \
))

def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(app_config[config_name])

	db.init_app(app)
	@app.route('/location/<name>', methods=["PUT","GET"])
	def location_request(name):
		if request.method == 'PUT':
			lat = request.get.latitude
			lon = request.get.longitude

			db.session.add(Location(
				request.get.name,
				lat,
				lon,
				fetch_elevaion( ( (lat, lon),) ),
			))
			
		if request.method == 'GET':
			r = db.Location.query.filter_by(name = request.get.name)
			return jsonify(r)

	@app.route('/closest', methods=["GET"])
	@app.route('/user/<user>/closest', methods=["GET"])
	def closest(user):
		lat = request.get.latitude
		lon = request.get.longitude
		r = db.Location.query().all()

		distances = getdistances(r,(lat,lon))

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
		r = db.Location.query().all()
		lat = request.get.latitude
		lon = request.get.longitude

		distances = getdistances(r, (lat,lon))
		radius = request.get.radius 
		f = filter( lambda x: x < radius, distances)
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

		return jsonify({"indistance": sresp, "radius": radius})
	
	return app
