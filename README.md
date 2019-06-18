# geodistanceAPI
Flask-RESTful API for geographical distance calculation.

The API let's is inserting a geographical position into a database along with their names.  Computing distances to these locations.  Finding the closest location form a given position.

Quickstart.
To run the api, create the environment and install nessesry packages.
```
virtualenv geodistanceapi
pip install -r requirements.txt
```
Afterwards, you need to initialize the database.
```
python -c "import run ; run.initialize_db()"
```

Now, set the configuration API will be running on,

```
export GEOAPI_SETTINGS="production"  
```
the API uses an elevation API (https://elevation-api.io/) so you need to provide a proper key.
```
export ELEVATION_API_IO_KEY="<YOUR_KEY>" 
```
Finally you can ran the API
```
python run.sh
```
