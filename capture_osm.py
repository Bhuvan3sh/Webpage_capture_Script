from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from PIL import Image
from io import BytesIO
import os


def capture_screenshot(url_template, output_folder, lat_range, lon_range, start_coordinates, end_coordinates, num_steps):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")

    with webdriver.Chrome(options=chrome_options) as driver:
        lat_step = (lat_range[1] - lat_range[0]) / num_steps
        lon_step = (lon_range[1] - lon_range[0]) / num_steps

        for i in range(num_steps):
            current_lat = lat_range[0] + i * lat_step
            current_lon = lon_range[0] + i * lon_step

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

            output_file = os.path.join(output_folder, f'screenshot_{i}.png')
            cropped_image.save(output_file)

            print(f"Iteration {i + 1} is completed, with url - {current_url}")

#varibales
url_template = 'https://www.openstreetmap.org/#map=17/{lat:.5f}/{lon:.5f}'
output_folder = 'D:/Progasm/venv/Open Street Maps/Output images'
lat_range = (40.81231, 40.80632)  # Define the range for latitude (start, end)
lon_range = (-77.86688, -77.84608)


#image crpoing
start_coordinates = (437, 195)
end_coordinates = (1870, 999)

num_steps = 100

os.makedirs(output_folder, exist_ok=True)
capture_screenshot(url_template, output_folder, lat_range, lon_range, start_coordinates, end_coordinates, num_steps)