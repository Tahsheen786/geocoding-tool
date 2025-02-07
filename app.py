from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests
import json

app = Flask(__name__)

# Replace with your OpenCage API key
API_KEY = "YOUR API KEY"

# Load location data from JSON
with open('location_data.json', encoding='utf-8') as f:
    location_data = json.load(f)

@app.route('/')
def index():
    countries = [country['name'] for country in location_data]
    return render_template('index.html', countries=countries)

@app.route('/states', methods=['POST'])
def states():
    country_name = request.json.get('country')
    country = next((c for c in location_data if c['name'] == country_name), None)
    if country:
        states = [state['name'] for state in country.get('states', [])]
    else:
        states = []
    return jsonify(states)

@app.route('/cities', methods=['POST'])
def cities():
    country_name = request.json.get('country')
    state_name = request.json.get('state')
    country = next((c for c in location_data if c['name'] == country_name), None)
    if country:
        state = next((s for s in country.get('states', []) if s['name'] == state_name), None)
        if state:
            cities = [city['name'] for city in state.get('cities', [])]
        else:
            cities = []
    else:
        cities = []
    return jsonify(cities)

def create_address(form):
    country = form.get('country')
    state = form.get('state')
    city = form.get('city')
    zip_code = form.get('zip_code')

    if zip_code:
        address = zip_code
    else:
        address_components = [country]
        if state:
            address_components.append(state)
        if city:
            address_components.append(city)
        address = ", ".join(address_components)

    return address

def get_location(address):
    base_url = "https://api.opencagedata.com/geocode/v1/json?"
    url = base_url + f"q={address}&key={API_KEY}"

    response = requests.get(url)
    response_data = response.json()

    if response.status_code == 200:
        if response_data['results']:
            location = response_data['results'][0]['geometry']
            latitude = location['lat']
            longitude = location['lng']
            return latitude, longitude
        else:
            print("No results found for the provided address.")
    else:
        print("Error fetching geocode data:", response.status_code)

    return None, None

@app.route('/weather', methods=['POST'])
def weather():
    address = create_address(request.form)
    latitude, longitude = get_location(address)
    if latitude is not None and longitude is not None:
        return jsonify({"latitude": latitude, "longitude": longitude})
    else:
        return jsonify({"error": "Error: Could not find location for the provided address."})


@app.route('/weather-result')
def weather_result():
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    return render_template('weather_result.html', latitude=latitude, longitude=longitude)

if __name__ == '__main__':
    app.run(debug=True)

