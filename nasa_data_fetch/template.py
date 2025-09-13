"""
📌 AppEEARS Data Fetch Template
This script allows you to fetch point-based satellite data from NASA's AppEEARS service.
You can specify:
    - Your NASA Earthdata Login credentials
    - Task date range
    - Product and layer
    - Coordinates
    - Output format (CSV)
"""

import requests
import time
import os

# ===========================
# 1️⃣ User Configuration
# ===========================

# Your NASA Earthdata Login credentials
USERNAME = "your_earthdata_username"
PASSWORD = "your_earthdata_password"

# Folder where CSVs will be saved
SAVE_FOLDER = r"Your_Directory_Address"  # <-- update this
os.makedirs(SAVE_FOLDER, exist_ok=True)

# Task parameters
TASK_NAME = "example_point_task"
START_DATE = "07-01-2024" # format: MM-DD-YYYY
END_DATE = "07-31-2024" #format: MM-DD-YYYY
LATITUDE = 35.5
LONGITUDE = -97.5
PRODUCT = "SPL4SMGP.008"          # e.g., SMAP, IMERG, MODIS NDVI, in this case Level-4 of SMAP version 008
LAYER = "Geophysical_Data_sm_rootzone"  # layer of the product
OUTPUT_FORMAT = "CSV"  # CSV or GeoTIFF

# ===========================
# 2️⃣ Login & Get AppEEARS Token
# ===========================

login_url = "https://appeears.earthdatacloud.nasa.gov/api/login"
response = requests.post(login_url, auth=(USERNAME, PASSWORD))
response.raise_for_status()
token_response = response.json()
TOKEN = token_response['token']
HEADERS = {"Authorization": f"Bearer {TOKEN}"}
print("✅ Logged in, token received")

# ===========================
# 3️⃣ Create a Task
# ===========================

task = {
    "task_type": "point",
    "task_name": TASK_NAME,
    "params": {
        "dates": [{"startDate": START_DATE, "endDate": END_DATE}],
        "layers": [{"layer": LAYER, "product": PRODUCT}],
        "coordinates": [{"latitude": LATITUDE, "longitude": LONGITUDE}],
        "output": {"format": OUTPUT_FORMAT}
    }
}

resp = requests.post("https://appeears.earthdatacloud.nasa.gov/api/task", headers=HEADERS, json=task)
resp.raise_for_status()
task_id = resp.json()['task_id']
print(f"✅ Task submitted: {task_id}")

# ===========================
# 4️⃣ Wait Until Task is Done
# ===========================

while True:
    status_resp = requests.get(f"https://appeears.earthdatacloud.nasa.gov/api/status/{task_id}", headers=HEADERS)
    status_resp.raise_for_status()
    status_json = status_resp.json()
    status = status_json.get('status') or status_json.get('task', {}).get('status')
    print(f"Task status: {status}")
    
    if status == "done":
        print("✅ Task is done")
        break
    time.sleep(10)  # Wait 10 seconds before polling again

# ===========================
# 5️⃣ Get Bundle Info
# ===========================

bundle_resp = requests.get(f"https://appeears.earthdatacloud.nasa.gov/api/bundle/{task_id}", headers=HEADERS)
bundle_resp.raise_for_status()
bundle = bundle_resp.json()
print("✅ Bundle info received")

# ===========================
# 6️⃣ Download CSV File
# ===========================

file_id = None
file_name = None

# Find the first CSV in the bundle
for f_info in bundle['files']:
    if f_info['file_type'].lower() == "csv":
        file_id = f_info['file_id']
        file_name = f_info['file_name']
        break

if file_id is None:
    raise ValueError("No CSV file found in the bundle!")

# Download the file (follow redirects to S3)
download_url = f"https://appeears.earthdatacloud.nasa.gov/api/bundle/{task_id}/{file_id}"
download_resp = requests.get(download_url, headers=HEADERS, allow_redirects=True, stream=True)
download_resp.raise_for_status()

filepath = os.path.join(SAVE_FOLDER, file_name)
with open(filepath, 'wb') as f:
    for chunk in download_resp.iter_content(chunk_size=8192):
        f.write(chunk)

print(f"✅ File saved to: {filepath}")
