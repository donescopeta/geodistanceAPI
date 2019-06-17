from app import create_app, db
import os
import sys

def initialize_db():
    with app.app_context():
        db.create_all()

config = os.getenv('APP_SETTINGS') 
if not config:
	config = "development" 
app = create_app(config)

if __name__ == '__main__':
    app.run()

