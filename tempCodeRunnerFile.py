@app.route('/weather', methods=['POST'])
def weather():
    country = request.form['country']
    state = request.form['state']
    city = request.form['city']
    zip_code = request.form['zip_code']
    if zip_code:
        address = zip_code
    else:
        address = f"{city}, {state}, {country}"
    lat, lon = get_location(address)
    if lat and lon:
        weather_data = get_weather_forecast(lat, lon, API_KEY)
        if weather_data:
            forecasts = weather_data['list'][:5]
            forecast_info = [
                {
                    "datetime": forecast['dt_txt'],
                    "temperature": forecast['main']['temp'],
                    "feels_like": forecast['main']['feels_like'],
                    "temp_min": forecast['main']['temp_min'],
                    "temp_max": forecast['main']['temp_max'],
                    "pressure": forecast['main']['pressure'],
                    "humidity": forecast['main']['humidity'],
                    "description": forecast['weather'][0]['description'],
                    "wind_speed": forecast['wind']['speed'],  # Add wind speed
                    "wind_deg": forecast['wind']['deg'],  # Add wind direction (degrees)
                    "clouds": forecast['clouds']['all'],
                }
                for forecast in forecasts
            ]

            # Redirect to weather forecast page with forecast info
            return redirect(url_for('weather_forecast', forecast_info=json.dumps(forecast_info)))
    return "Error fetching weather data"

@app.route('/weather-forecast')
def weather_forecast():
    forecast_info = json.loads(request.args.get('forecast_info'))
    return render_template('weather_forecast.html', forecast_info=forecast_info)
