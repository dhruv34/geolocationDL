import os
import requests
import pandas as pd
import random
from pathlib import Path

API_KEY = "AIzaSyD9lnKsRB9QutRMVbuqgKScMcuarCmcPA4"
data_path = Path("./data/dataframes")
output_folder = Path("./places_api_data")
output_folder.mkdir(exist_ok=True)

def get_random_images_for_city(city_name, lat, lon, radius, api_key, num_images=20):
    places_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    images = []

    # 1. Fetch places
    response = requests.get(places_url, params={
        "location": f"{lat},{lon}",
        "radius": radius,
        "type": "point_of_interest",
        "key": api_key
    })

    response_data = response.json()
    if response_data.get('status') != 'OK':
        print(f"Error in Places API response for {city_name}: {response_data.get('status')}")
        return images

    places = response_data.get('results', [])
    if not places:
        print(f"No places found for {city_name}.")
        return images

    # 2. Randomly sample places (limit to 20 if needed)
    selected_places = random.sample(places, min(len(places), num_images))

    # 3. Fetch photos for each place
    city_folder = output_folder / city_name
    city_folder.mkdir(exist_ok=True)

    for i, place in enumerate(selected_places):
        if 'photos' in place:
            photo_reference = place['photos'][0]['photo_reference']
            photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={api_key}"

            photo_response = requests.get(photo_url)
            if photo_response.status_code == 200:
                image_filename = city_folder / f"{city_name}_image_{i + 1}.jpg"
                with open(image_filename, "wb") as img_file:
                    img_file.write(photo_response.content)
                images.append(image_filename)

    print(f"{len(images)} images saved for {city_name}.")
    return images

# Default radius (e.g., 5000 meters) for each city
DEFAULT_RADIUS = 5000

# Process each CSV file in the ./data/dataframes directory
for city_file in data_path.glob("*.csv"):
    city_name = city_file.stem  # Extract city name from the file name (e.g., Medellin)
    try:
        # Load CSV file and extract latitude and longitude from the first row
        city_data = pd.read_csv(city_file)
        lat = city_data['lat'].iloc[0]
        lon = city_data['lon'].iloc[0]

        # Generate images for the city
        get_random_images_for_city(city_name, lat, lon, DEFAULT_RADIUS, API_KEY)

    except Exception as e:
        print(f"Error processing {city_name}: {e}")
