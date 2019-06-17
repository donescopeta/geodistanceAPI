from app import create_app, db
from tests import test_elevation_api
import pytest

locations = tuple( test_elevation_api.load_locations() )

test_locations = (
    #Latitude  Longitude  Closest
    (50.98660, 23.172646, "Lublin"), # <- Krasnystaw 
    (52.409161, 20.937183,"Warsaw"), # <- Legionwo
    (55.853582, -4.244692, "London") # <- Glasgow
)      

@pytest.fixture(scope="module")
def app():
    app = create_app(config_name="testing")
    with app.app_context():
        db.create_all()
        return app

@pytest.fixture(scope="module")
def client(app):
    return app.test_client()


@pytest.mark.incremental
class TestFlaskAPI(object):

    def test_inserting_loaction_into_database(self, client):

        for latitude, longitude, name in locations:
            res = client.put('/location/%s' % name, data = { 
                "latitude":latitude,
                "longitude":longitude
            })
            json = res.get_json()
            assert json is not None
            assert json["message"] == "success"

    def test_fetching_from_api_by_name(self, client):

        for latitude, longitude, name in locations:

            res = client.get( '/location/%s' % name ).get_json()
            assert \
                res["latitude"] == latitude and \
                res["longitude"] == longitude and \
                res["name"] == name

    def test_finding_closest_locations(self, client):

        for lat, lon, closest in test_locations:
            res = client.get('/closest',query_string = {
                "latitude" : lat, 
                "longitude" : lon
            }).get_json()
            assert res is not None
            assert res["closest"]["name"] == closest

    def test_finding_locations_in_given_distance(self, client):
        
        #Krasnystaw, 60 km radius, should result Lublin.     
        res = client.get('indistanceof', query_string = {
            "latitude": 50.98660,
            "longitude": 23.172646,
            "radius": 60 * 1000
        }).get_json()["indistance"]
        
        assert res is not None
        assert res[0]["name"] == "Lublin"

        #Krasnystaw, 400 km radius, should result Lublin, Warsaw, Radom.     
        res = client.get('/indistanceof', query_string = {
            "latitude" : 50.98660,
            "longitude" : 23.172646,
            "radius" : 400 * 1000
        }).get_json()["indistance"]


        assert res is not None        
        assert set([ x["name"] for x in res ]) == set(("Lublin", "Warsaw", "Radom"))

        #Krasnystaw, 0.002 km radius, should result nothing.     

        res = client.get('/indistanceof', query_string = {
            "latitude" : 50.98660,
            "longitude" : 23.172646,
            "radius" : 2
        }).get_json()["indistance"]

        assert res is not None        
        assert not res

