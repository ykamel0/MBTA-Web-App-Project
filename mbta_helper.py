import os
import json
import urllib.request
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API keys from environment variables
MAPBOX_TOKEN = os.getenv("MAPBOX_API_KEY")
MBTA_API_KEY = os.getenv("MBTA_API_KEY")

# Useful base URLs (you need to add the appropriate parameters for each API request)
MAPBOX_BASE_URL = "https://api.mapbox.com/geocoding/v5/mapbox.places"
MBTA_BASE_URL = "https://api-v3.mbta.com/stops"


def get_json(url: str, headers=None) -> dict:
    """
    Given a properly formatted URL for a JSON web API request, return a Python JSON object containing the response to that request.
    """
    # Add a User-Agent header to avoid HTTP 403 errors
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0')

    # Add additional headers if provided
    if headers:
        for key, value in headers.items():
            req.add_header(key, value)

    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode("utf-8"))
        return data
    except urllib.error.HTTPError as e:
        print(f"HTTPError: {e.code} - {e.reason}")
        return {}
    except urllib.error.URLError as e:
        print(f"URLError: {e.reason}")
        return {}
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {}


def get_lat_lng(place_name: str) -> tuple:
    """
    Given a place name or address, return a (latitude, longitude) tuple with the coordinates of the given place.

    See https://docs.mapbox.com/api/search/geocoding/ for Mapbox Geocoding API URL formatting requirements.
    """
    # Format the place name to be URL safe
    place_name = place_name.replace(" ", "%20")
    # Construct the Mapbox API URL
    url = f"{MAPBOX_BASE_URL}/{place_name}.json?access_token={MAPBOX_TOKEN}"
    # Get the JSON response
    data = get_json(url)
    
    if not data or "features" not in data or not data["features"]:
        print(f"Could not find location for '{place_name}'.")
        raise ValueError(f"Could not find location for '{place_name}'.")

    # Extract latitude and longitude from the response
    coordinates = data["features"][0]["geometry"]["coordinates"]
    return coordinates[1], coordinates[0]  # Returning (latitude, longitude)


def get_nearest_station(latitude: str, longitude: str) -> tuple:
    """
    Given latitude and longitude strings, return a (station_name, wheelchair_accessible) tuple for the nearest MBTA station to the given coordinates.

    See https://api-v3.mbta.com/docs/swagger/index.html#/Stop/ApiWeb_StopController_index for URL formatting requirements for the 'GET /stops' API.
    """
    # Construct the MBTA API URL
    url = f"{MBTA_BASE_URL}?filter[latitude]={latitude}&filter[longitude]={longitude}&sort=distance"
    headers = {
        "Authorization": f"Bearer {MBTA_API_KEY}"
    }
    # Get the JSON response
    data = get_json(url, headers=headers)

    if not data or "data" not in data or not data["data"]:
        print(f"No MBTA station found near latitude {latitude} and longitude {longitude}.")
        raise ValueError(f"No MBTA station found near latitude {latitude} and longitude {longitude}.")

    # Extract the nearest station information
    nearest_station = data["data"][0]
    station_name = nearest_station["attributes"]["name"]
    wheelchair_accessible = nearest_station["attributes"]["wheelchair_boarding"] == 1
    return station_name, wheelchair_accessible


def find_stop_near(place_name: str) -> tuple:
    """
    Given a place name or address, return the nearest MBTA stop and whether it is wheelchair accessible.
    """
    # Get latitude and longitude for the given place name
    latitude, longitude = get_lat_lng(place_name)
    # Get the nearest MBTA station based on latitude and longitude
    return get_nearest_station(latitude, longitude)


def main():
    """
    You should test all the above functions here.
    """
    place = "Boston Common"
    try:
        station_name, accessible = find_stop_near(place)
        print(f"Nearest MBTA Station to {place}: {station_name}, Wheelchair Accessible: {accessible}")
    except ValueError as e:
        print(e)


if __name__ == "__main__":
    main()