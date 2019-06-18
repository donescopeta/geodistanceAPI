# geodistanceAPI
Flask-RESTful API for geographical distance calculation.

The API lets you insert a geographical position into a database along with their names. Computing distances to these locations.  Finding the closest location form a given position.


## Quickstart.
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
Finally, you can run the API.
```
python run.sh
```

## Running Tests
virtualenv geodistanceapi # if you you use virtualenv
```
 python -m pytest tests/
```
## Usage.

### Adding new locations.
You can add a new location to a database using a PUT request to ```/location/<location_name>```
```
curl -X PUT -d 'latitude=51.228231&longitude=22.581397' http://localhost:5000/location/Lublin
curl -X PUT -d 'latitude=52.237464&longitude=21.013131' http://localhost:5000/location/Warsaw
```
### Fetching an existing location.
```
curl -X GET http://localhost:5000/location/Lublin
```
API response 
```
{
  "elevation": 180,{
  "elevation": 180,
  "latitude": 51.228231,
  "longitude": 22.581397,
  "name": "Lublin"
}
```
### Requesting the closest location to a given position.
```
curl -X GET 'http://localhost:5000/closest?latitude=53.228231&longitude=27.581397'
```
API responce 
```
{
  "closest": {
    "distance": 407586.37341424276,
    "elevation": 180,
    "latitude": 51.228231,
    "longitude": 22.581397,
    "name": "Lublin"
  }
}
```
### Requesting all locations in a given distance from the position.
```
curl -X GET 'http://localhost:5000/indistanceof?radius=3000000&latitude=53.228231&longitude=27.581397'
```
Radius attribute must contain a distance in meters.

 API Responce
 ```
{
  "indistance": [
    {
      "distance": 407586.37341424276,
      "elevation": 180,
      "latitude": 51.228231,
      "longitude": 22.581397,
      "name": "Lublin",
      "order": 0
    },
    {
      "distance": 457003.0236602798,
      "elevation": 110,
      "latitude": 52.237464,
      "longitude": 21.013131,
      "name": "Warsaw",
      "order": 1
    }
  ],
  "radius": 3000000
}
 ```
