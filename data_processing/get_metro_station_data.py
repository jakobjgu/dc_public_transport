"""
This data is fetched via different WMATA APIs. As an API key I used the publicly available test-key from the
WMATA API website.
'https://developer.wmata.com/api-details#api=5476364f031f590f38092507&operation=5476364f031f5909e4fe330c'
"""

import requests
import pandas as pd
import sys
from pathlib import Path

# Add your local modules
sys.path.append("../dc_metro")

from settings import WMATA_DEMO_API_KEY

# Output path
output_csv = Path("../dc_metro/source_files/metro_data/station_coordinates.csv")

# Set up API request headers
headers = {"api_key": WMATA_DEMO_API_KEY}

try:
    # Get all metro lines
    line_url = "https://api.wmata.com/Rail.svc/json/jLines"
    response = requests.get(line_url, headers=headers)
    response.raise_for_status()
    line_codes = [line["LineCode"] for line in response.json()["Lines"]]

    station_coords = []

    # Loop through lines and fetch stations per line
    for line_code in line_codes:
        station_url = f"https://api.wmata.com/Rail.svc/json/jStations?LineCode={line_code}"
        r = requests.get(station_url, headers=headers)
        r.raise_for_status()
        stations = r.json()["Stations"]

        for s in stations:
            station_coords.append({
                "station_name": s["Name"],
                "station_id":s["Code"],
                "lat": s["Lat"],
                "lon": s["Lon"],
                "line": line_code
            })

    # Create DataFrame and drop duplicate stations (since many appear on multiple lines)
    station_df = pd.DataFrame(station_coords).drop_duplicates(subset=["station_name", "lat", "lon", "line"])

    # Export to CSV
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    station_df.to_csv(output_csv, index=False)
    print(f"Station coordinate data saved to {output_csv.resolve()}")

except Exception as e:
    print("An error occurred:", e)
