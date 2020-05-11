import requests
import json
from flask import Flask, abort

app = Flask(__name__)

geocoding_service_url = "https://eu1.locationiq.com/v1/search.php?key=2081a221a6f6c1&q={}&format=json"
weather_forecast_service_url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&appid=d5c7b57b52b8d215f80cd10650232f5e&units=metric&lang=tr"


@app.route('/geocode/<city>', methods=['GET'])
def geocode(city):
    content = requests.get(geocoding_service_url.format(city)).content
    info = json.loads(content)
    if "error" in info:
        abort(404)

    lat = float(info[0]["lat"])
    lon = float(info[0]["lon"])
    return json.dumps({"lat": lat, "lon": lon})


@app.route('/forecast/<city>', methods=['GET'])
def forecast(city):
    info = geocode(city)
    info = json.loads(info)
    lat = info["lat"]
    lon = info["lon"]
    content = requests.get(weather_forecast_service_url.format(lat, lon)).content
    content = json.loads(content)
    weather_info = {"current": content["current"], "daily": content["daily"]}
    return json.dumps(weather_info)


if __name__ == '__main__':
    app.run()
