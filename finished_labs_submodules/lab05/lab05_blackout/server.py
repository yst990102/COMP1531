from flask import Flask, request
from json import dump, dumps
from math import pi

from blackout import City, Satellite, check_blackout, update_satellite

app = Flask(__name__)

# Write your routes here
cities = []
satellites = []


@app.route('/city', methods=['POST'])
def city():
    city_data = request.get_json()
    city_name = city_data["name"]
    city_theta = city_data["theta"]

    cities.append(City(city_name, city_theta))

    return dumps({})


@app.route('/satellite', methods=['POST'])
def satellite():
    satellite_data = request.get_json()
    satellite_height = satellite_data['height']
    satellite_velocity = satellite_data['velocity']
    satellite_theta = satellite_data['theta']

    satellites.append(Satellite(satellite_height, satellite_velocity, satellite_theta))
    return dumps({})


@app.route('/simulate', methods=['GET'])
def simulate():
    sim_list = []
    for city in cities:
        city.intervals = 0

    for i in range(0, 1440):
        for satellite in satellites:
            update_satellite(satellite)

        for city in cities:
            blackout = True
            for satellite in satellites:
                blackout = blackout and check_blackout(city, satellite)

            if blackout == True:
                city.intervals += 1
    for city in cities:
        sim_list.append((city.name, city.intervals))

    return dumps({"cities": sorted(sim_list)})


if __name__ == '__main__':
    app.run(port=0)