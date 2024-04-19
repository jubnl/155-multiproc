import threading
import time

import requests
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
weather_data = {}
api_key = "31cb0993c8054df9ae7120723241503"
weather_data_lock = threading.Lock()
active_threads = {}

thread_id = time.time()


def fetch_weather_data(city):
    global weather_data
    global thread_id
    while thread_id == active_threads.get(city)[0]:
        with weather_data_lock:
            data = requests.get(
                f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}").json()
            if "error" in data.keys():
                data["success"] = False
            else:
                data["success"] = True
            print(data)
            weather_data[city] = data
        time.sleep(5)


@app.route('/weather')
def get_weather():
    global thread_id
    city = request.args.get('city', "ERROR")
    if city == "ERROR":
        return jsonify({
            "success": False,
            "error": {
                "code": 400,  # randomly chosen
                "message": "Please provide a city name"
            }
        })
    if city in active_threads:
        active_threads[city][1].join()

        # Create a new thread for the new city
        fetch_thread = threading.Thread(target=fetch_weather_data, args=(city,))
        fetch_thread.daemon = True
        fetch_thread.start()
        active_threads[city] = (thread_id, fetch_thread)
        time.sleep(1)

    with weather_data_lock:
        print(active_threads)
        print(weather_data)
        return jsonify(weather_data.get(city, {
            "success": False,
            "error": {
                "code": 400,  # randomly chosen
                "message": "Please provide a city name"
            }
        }))


if __name__ == '__main__':
    app.run(debug=True, port=8000, host="0.0.0.0")
