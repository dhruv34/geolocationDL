#Akshay API KEY: AIzaSyD9lnKsRB9QutRMVbuqgKScMcuarCmcPA4
import requests

# Define API URL and parameters
base_url = "https://maps.googleapis.com/maps/api/streetview"
params = {
    "size": "600x400",
    "location": "40.758896,-73.985130",  # Example coordinates (Times Square)
    "heading": "90",
    "pitch": "10",
    "key": "AIzaSyD9lnKsRB9QutRMVbuqgKScMcuarCmcPA4"  # Replace with your actual API key
}

# Send GET request to the Street View API
response = requests.get(base_url, params=params)

# Save image if request is successful
if response.status_code == 200:
    with open("streetview_image.jpg", "wb") as file:
        file.write(response.content)
    print("Image saved as 'streetview_image.jpg'")
else:
    print("Error:", response.status_code, response.text)
