"""
The original xlxs files used for this project were downloaded from
'https://planitmetro.com/2012/10/31/data-download-metrorail-ridership-by-origin-and-destination/'
"""

import pandas as pd
import sys
sys.path.append("../dc_metro")
from settings import (
    PROJECT_SOURCE_FILES_DIR
    )

# Define directory paths
csv_file_output_dir = f"{PROJECT_SOURCE_FILES_DIR}/metro_data/"

def prepare_ridership_data():
    metro_weekday = pd.read_excel(
        csv_file_output_dir + "May-2012-Metrorail-OD-Table-by-Time-of-Day-and-Day-of-Week.xlsx",
        sheet_name="Weekday",
        engine="openpyxl",
        header=2)
    metro_weekday.rename(
        columns={
            "Ent Station":"ent_station",
            "Ext Station":"ext_station",
            "Ent Time Period":"ent_time_period",
            "Riders, Average Weekday, May 2012":"riders_average_weekday"
    }, inplace=True)

    metro_saturday = pd.read_excel(
        csv_file_output_dir + "May-2012-Metrorail-OD-Table-by-Time-of-Day-and-Day-of-Week.xlsx",
        sheet_name="Saturday",
        engine="openpyxl",
        header=2)
    metro_saturday.rename(
        columns={
            "Ent Station":"ent_station",
            "Ext Station":"ext_station",
            "Ent Time Period":"ent_time_period",
            "Riders, Average Saturday, May 2012":"riders_average_saturday"
    }, inplace=True)

    metro_sunday = pd.read_excel(
        csv_file_output_dir + "May-2012-Metrorail-OD-Table-by-Time-of-Day-and-Day-of-Week.xlsx",
        sheet_name="Sunday",
        engine="openpyxl",
        header=2)
    metro_sunday.rename(
        columns={
            "Ent Station":"ent_station",
            "Ext Station":"ext_station",
            "Ent Time Period":"ent_time_period",
            "Riders, Average Sunday, May 2012":"riders_average_sunday"
    }, inplace=True)

    metro_late_night = pd.read_excel(
        csv_file_output_dir + "May-2012-Metrorail-OD-Table-by-Time-of-Day-and-Day-of-Week.xlsx",
        sheet_name="Late-Night Peak",
        engine="openpyxl",
        header=2)
    metro_late_night.rename(
        columns={
            "Ent Station":"ent_station",
            "Ext Station":"ext_station",
            "Ent Time Period":"ent_time_period",
            "Riders, Average Late-night, May 2012":"riders_average_weekday_late_night"
    }, inplace=True)

    # Define the path for the output files
    weekday_output_file = f"{csv_file_output_dir}weekday_ridership.csv"
    saturday_output_file = f"{csv_file_output_dir}saturday_ridership.csv"
    sunday_output_file = f"{csv_file_output_dir}sunday_ridership.csv"
    late_night_output_file = f"{csv_file_output_dir}late_night_ridership.csv"

    # output df
    metro_weekday.to_csv(weekday_output_file, index=False)
    metro_saturday.to_csv(saturday_output_file, index=False)
    metro_sunday.to_csv(sunday_output_file, index=False)
    metro_late_night.to_csv(late_night_output_file, index=False)

if __name__ == "__main__":
    print("Main is triggered")
    prepare_ridership_data()