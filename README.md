# 🛰 NASA Data Fetch - Space2Soil Backend

This module allows fetching **point-based satellite data** from NASA's **AppEEARS** service for a specific location and time period.

It is designed as a **template** and will be used in our upcoming game for environmental and soil data simulation.

---

## 📂 Current Structure

<pre> ```text space2soil_backend/ └── nasa_data_fetch/ ├── template.py # Fetches satellite data via AppEEARS └── requirements.txt # Required Python libraries (currently: requests) ``` </pre>

## Configure template.py:

### Update the following fields in the script:

```
USERNAME = "your_earthdata_username"
PASSWORD = "your_earthdata_password"
SAVE_FOLDER = r"Your_Directory_Address"

TASK_NAME = "example_point_task"
START_DATE = "MM-DD-YYYY"
END_DATE = "MM-DD-YYYY"
LATITUDE = 35.5
LONGITUDE = -97.5
PRODUCT = "SPL4SMGP.008"          # e.g., SMAP, IMERG, NDVI
LAYER = "Geophysical_Data_sm_rootzone"
OUTPUT_FORMAT = "CSV"
```

## Notes

- Only point-based data is supported currently.

- The script automatically polls the task until completion and downloads the resulting CSV.

- CSV files contain timestamped data for the selected location and product/layer.

- This module will be integrated into the game to provide real-world satellite data for simulation.
