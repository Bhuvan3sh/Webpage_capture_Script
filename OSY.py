'''
Author - A Bhuvanesh
Github - https://github.com/Bhuvan3sh
Mai@id - abhuavnesh501@gmail.com
Dependicies -   selenium
                time
                PIL
                io
                os
                yaml
'''

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from PIL import Image
from io import BytesIO
import os
import yaml

def load_coordinates(file_path):
    with open(file_path, 'r') as file:
        coordinates = yaml.safe_load(file)
    return coordinates

def capture_screenshot(url_template, output_folder, location, lat_steps, lon_steps, start_coordinates, end_coordinates):
    lat_range = location['lat_range']
    lon_range = location['lon_range']

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")

    with webdriver.Chrome(options=chrome_options) as driver:
        for lon_index in range(lon_steps):
            current_lon = lon_range[0] + lon_index * (lon_range[1] - lon_range[0]) / lon_steps

            for lat_index in range(lat_steps):
                current_lat = lat_range[0] + lat_index * (lat_range[1] - lat_range[0]) / lat_steps

                current_url = url_template.format(lat=current_lat, lon=current_lon)
                driver.get(current_url)

                time.sleep(5)

                driver.set_window_size(1920, 1020)
                driver.execute_script(f"window.scrollTo({start_coordinates[0]}, {start_coordinates[1]});")
                screenshot = driver.get_screenshot_as_png()

                image = Image.open(BytesIO(screenshot))
                x1, y1 = start_coordinates
                x2, y2 = end_coordinates
                cropped_image = image.crop((x1, y1, x2, y2))

                output_file = os.path.join(output_folder, f'screenshot_{location["name"]}_lon_{lon_index}_lat_{lat_index}.png')
                cropped_image.save(output_file)

                print(f"Iteration (Location: {location['name']}, Longitude: {lon_index + 1}, Latitude: {lat_index + 1}) completed, with url - {current_url}")

# Variables
url_template = 'https://www.openstreetmap.org/#map=17/{lat:.5f}/{lon:.5f}'
output_folder = 'D:/Progasm/venv/OSM_Y/OUT IMAGES'

start_coordinates = (437, 195)
end_coordinates = (1870, 999)


lat_steps = 8
lon_steps = 8

# YAML file config
coordinates_file = 'OSM.yml'
locations = load_coordinates(coordinates_file)

os.makedirs(output_folder, exist_ok=True)
for location in locations:
    capture_screenshot(url_template, output_folder, location, lat_steps, lon_steps, start_coordinates, end_coordinates)