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
python run.py
```

## Running Tests
```
# if you you use virtualenv
virtualenv geodistanceapi 
python -m pytest tests/
```
## Usage.

### Adding new locations.
You can add a new location to a database using a PUT method to ```/location/<location_name>```
```
curl -X PUT -d 'latitude=51.228231&longitude=22.581397' http://localhost:5000/location/Lublin
curl -X PUT -d 'latitude=52.237464&longitude=21.013131' http://localhost:5000/location/Warsaw
```
or
```
./geodistancecli add Lublin 51.228231 22.581397
./geodistancecli add Warsaw 52.237464 21.013131
```
#### Details:
* URL: ```/location/:name```
* Method: PUT
* Data params: latitude, longitude
* Required: latitude=[float] , longitude=[float]
* Success Response: 201
* Error Response: 400

### Fetching an existing location.
```
curl -X GET http://localhost:5000/location/Lublin
```
or
```
./geodistancecli get Lublin
```
API response 
```
{
  "elevation": 180,
  "latitude": 51.228231,
  "longitude": 22.581397,
  "name": "Lublin"
}

```
#### Details:
* URL: ```/location/:name```
* Method: GET
* Success Response: 201, 204

### Requesting the closest location to a given position.
```
curl -X GET 'http://localhost:5000/closest?latitude=53.228231&longitude=27.581397'
```

or
```
./geodistancecli closest 53.228231 27.581397
```
API response 
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
#### Details:
* URL: ```/location/closest```
* Method: GET
* URL Params: latitude, longitude
* Required: latitude=[float] , longitude=[float]
* Success Response: 200, 204
* Error Response: 400

### Requesting all locations in a given distance from the position.
```
curl -X GET 'http://localhost:5000/indistanceof?radius=3000000&latitude=53.228231&longitude=27.581397'
```
or

```
./geodistancecli indistance 3000000 53.228231 27.581397
```

Radius attribute must contain a distance in meters.

 API response
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

#### Details:
* URL: ```/location/indistance```
* Method: GET
* URL Params: latitude, longitude, radius
* Required: latitude=[float] , longitude=[float], radius=[float] ,
* Success Response: 200
* Error Response: 400
