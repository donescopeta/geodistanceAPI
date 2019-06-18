#!flask/bin/python
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from model import db, Location, User 
from elevation import fetch_elevaion
from geopy import distance

from config import app_config

get_distances_form_query = lambda rows, location, dist = lambda x: distance.vincenty(*x).meters: \
    tuple(map( dist, \
        map(lambda x: (
            (x.latitude, x.longitude),
            location
        ), rows) \
    ))

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    
    db.init_app(app)

    @app.route('/location/<name>', methods=["PUT","GET"])
    def location_request(name):
        """Function that handles appending or fetching a location."""
        print (request.form)
        if request.method == 'PUT':
            try:
                lat = float(request.form["latitude"])
                lon = float(request.form["longitude"])
            except: return "", 400 # <- Bad request

            db.session.add(Location(
                name = name,
                latitude = lat,
                longitude = lon,
                elevation  = fetch_elevaion( ( (lat, lon),) )[0],
            ))

            db.session.commit()
            return jsonify({ "message" : "success" }), 201

        if request.method == 'GET':
            d = db.session.query(Location).filter_by(name = name).first()
            if not d :
                return '{}', 204
            return jsonify({
                "name": d.name,
                "latitude": d.latitude,
                "longitude": d.longitude,
                "elevation": d.elevation, 
            }), 200

    @app.route('/closest', methods=["GET"])
    @app.route('/user/<user>/closest', methods=["GET"])
    def closest_request(user = None):
        """ This function processees request for the closest location avaiable."""
        try:
            lat = float(request.args.get("latitude"))
            lon = float(request.args.get("longitude"))
        except: return "{}", 400 # <- Bad request
            
        r =  db.session.query(Location).all()

        distances = get_distances_form_query(r,(lat,lon))

        if not distances:
            return jsonify( {"closest": {}, }), 204

        # looking for minimal distance
        min_d = sorted(distances)[0]
        d = r[distances.index(min_d)]

        return jsonify({"closest": {
            "name": d.name,
            "latitude": d.latitude,
            "longitude": d.longitude,
            "elevation": d.elevation, 
            "distance": min_d
        }}), 200


    @app.route('/indistanceof', methods=["GET"])
    @app.route('/user/<user>/indistanceof', methods=["GET"])
    def indistanceof_request(user = None):
        """ This function processes the request for a list of
            locations in a certain radius from a given position
        """

        try:
            lat = float(request.args.get("latitude"))
            lon = float(request.args.get("longitude"))
            radius = float(request.args.get("radius"))
        except: return "", 400 # <- Bad request
            
        r = db.session.query(Location).all()
        distances = get_distances_form_query(r, (lat,lon))
        f = sorted( filter( lambda x: x and x < radius, distances) )
        resp = []

        for x, n in zip(sorted(f), range(len(f))):
            d = r[distances.index(x)]
            resp.append({
                "name": d.name,
                "latitude": d.latitude,
                "longitude": d.longitude,
                "elevation": d.elevation, 
                "distance": x,
                "order": n
            })

        return jsonify({"indistance": resp, "radius": radius}), 200
    
    return app
