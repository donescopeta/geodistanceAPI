from app import create_app
import os

try:
	config = os.getenv('APP_SETTINGS') 
except:
	config = "development" 
app = create_app(config)

if __name__ == '__main__':
    app.run()

