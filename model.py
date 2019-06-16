from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Location(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     name = db.Column(db.String)
     latitude = db.Column(db.Float)
     longitude = db.Column(db.Float)
     elevation = db.Column(db.Float)

class User(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     name = db.Column(db.String)
     latitude = db.Column(db.Float)
     longitude = db.Column(db.Float)
     hash = db.Column(db.String)
