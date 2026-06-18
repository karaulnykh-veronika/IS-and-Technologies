import geocoder
import requests
from datetime import date



def get_city_coordinates(city_name):
    city = geocoder.arcgis("Иркутск")
    latitude = city.json['lat']
    longitude = city.json['lng']
    return (latitude, longitude)



# return today date in format yyyy-mm-dd
def get_today_date():
    today = date.today()
    return f"{today.year:04d}-{today.month:02d}-{today.day:02d}"



def request_sunrise_sunset_daylen_info(latitude, longitude, date):
    url = "https://api.sunrise-sunset.org/json"
    params = {
        "lat": latitude,
        "lng": longitude,
        "date": date
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise Exception("Error: request to sunrise-sunset.org API is not successful.")
    response_dict = response.json()["results"]
    day_len = response_dict["day_length"]
    sunrise = response_dict["sunrise"]
    sunset = response_dict["sunset"]
    return (sunrise, sunset, day_len)



# open-meteo API works without api_key etc.
# pass date in format yyyy-mm-dd 
def request_day_night_temperature(latitude, longitude, date):
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": date,
        "end_date": date,
        "daily": "temperature_2m_max,temperature_2m_min",
        "timezone": "auto"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    
    day_temperature = response.json()["daily"]["temperature_2m_max"][0]
    night_temperature = response.json()["daily"]["temperature_2m_min"][0]
    return (day_temperature, night_temperature)



def main():
    print("Sunrise and sunset time, day length in Irkutsk today!")
    latitude, longitude = get_city_coordinates("Irkutsk")
    today = get_today_date()
    try:
        sunrise, sunset, day_len = request_sunrise_sunset_daylen_info(latitude, longitude, today)
        print(f"Sunrise time: {sunrise} UTC")
        print(f"Sunset time: {sunset} UTC")
        print(f"Day length: {day_len}") 

        day_temp, night_temp = request_day_night_temperature(latitude, longitude, "2025-03-24")
        print(f"Day temperature: {day_temp}℃")
        print(f"Night temperature: {night_temp}℃")
    except Exception as e:
        print(e)



if __name__ == "__main__":
    main()
