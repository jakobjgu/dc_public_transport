"""
THe data used in this script is a combination of the station data retrieved from WMATA in
this script (get_metro_station_data.py) and stations-per-line data copy/pasted from Wikipedia
and then cleaned in this script (metro_analytics.ipynb).
"""

import pandas as pd
import boto3
import sys
sys.path.append("../dc_public_transport")
sys.path.append("../dc_public_transport/data_processing")
from settings import (
    S3_BUCKET,
    PROJECT_SOURCE_FILES_DIR
    )
from utils.metro_station_name_corrections import load_station_name_corrections, normalize_and_correct_name

# Define directory paths
csv_file_output_dir = f"{PROJECT_SOURCE_FILES_DIR}/metro_data/"
path_to_name_corrections_csv = f"{PROJECT_SOURCE_FILES_DIR}/metro_data/station_name_corrections.csv"

def prepare_station_data(s3_client):
    station_data = pd.read_csv(
        csv_file_output_dir + "cleaned_stations.csv",
        header=0)
    station_data.rename(
        columns={
            "Station Name":"station_name",
            "Station ID":"station_id",
            "Metroline":"metroline"
    }, inplace=True)

    wmata_data = pd.read_csv(
        csv_file_output_dir + "station_coordinates.csv",
        header=0
        )
    
    # Standardize line codes (WMATA uses 2-letter codes)
    line_code_map = {
        "RD": "red",
        "BL": "blue",
        "YL": "yellow",
        "OR": "orange",
        "GR": "green",
        "SV": "silver"
    }
    wmata_data["metroline"] = wmata_data["line"].map(line_code_map)

    corrections = load_station_name_corrections(path_to_name_corrections_csv)
    wmata_data["station_name_clean"] = wmata_data["station_name"].apply(lambda x: normalize_and_correct_name(x, corrections))
    station_data["station_name_clean"] = station_data["station_name"].apply(lambda x: normalize_and_correct_name(x, corrections))

    # Merge on cleaned name and line
    merged = pd.merge(
        station_data,
        wmata_data,
        how="left",
        on=["station_id"],
        suffixes=["_st", "_WMATA"]
    )

    # Check missing coords
    missing = merged[merged["lat"].isnull()]
    if not missing.empty:
        # print("Stations with missing coordinates:")
        # print(missing[["station_name_clean"]])
        print(missing.head(5))

    # Define the path for the output files
    station_output_file = f"{csv_file_output_dir}station_line_map.csv"

    # Trim output df
    cols_to_keep = ['station_name_clean_st','station_id','metroline_st','lat','lon']
    merged = merged[cols_to_keep].copy()
    merged.rename(columns={"station_name_clean_st":"station_name",
                           "metroline_st":"metroline"}, inplace=True)
    merged.drop_duplicates(subset=["station_name", "lat", "lon", "metroline"], inplace=True)

    # output df
    merged.to_csv(station_output_file, index=False)

    # print("Attempting to push csv file to S3")
    try:
        s3_client.upload_file(station_output_file, S3_BUCKET, f"metro/raw/station_line_map.csv")
        print("Finished pushing csv file to S3")
    except Exception as e:
        print(f"Push to S3 unsuccessful because: {e}")

if __name__ == "__main__":
    print("Main is triggered")
    s3_client = boto3.client("s3")  # Create client for manual execution
    prepare_station_data(s3_client)