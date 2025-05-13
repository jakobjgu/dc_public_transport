import networkx as nx
import matplotlib.pyplot as plt
import pickle
import pandas as pd
import boto3
import sys
sys.path.append("../dc_metro")
from settings import (
    PROJECT_SOURCE_FILES_DIR,
    PROJECT_TRANSFORMED_FILES_DIR,
    S3_BUCKET
    )

from utils.metro_station_name_corrections import load_station_name_corrections, normalize_and_correct_name

def add_shortest_trip_length(s3_client):
    # Define the path for the input and output files
    path_to_name_corrections_csv = f"{PROJECT_SOURCE_FILES_DIR}/metro_data/station_name_corrections.csv"
    station_input_file = f"{PROJECT_SOURCE_FILES_DIR}/metro_data/station_line_map.csv"

    weekday_input_file = f"{PROJECT_SOURCE_FILES_DIR}/metro_data/weekday_ridership.csv"
    saturday_input_file = f"{PROJECT_SOURCE_FILES_DIR}/metro_data/saturday_ridership.csv"
    sunday_input_file = f"{PROJECT_SOURCE_FILES_DIR}/metro_data/sunday_ridership.csv"
    late_night_input_file = f"{PROJECT_SOURCE_FILES_DIR}/metro_data/late_night_ridership.csv"
    
    weekday_output_file = f"{PROJECT_SOURCE_FILES_DIR}/metro_data/weekday_ridership_with_trip_length.csv"
    saturday_output_file = f"{PROJECT_SOURCE_FILES_DIR}/metro_data/saturday_ridership_with_trip_length.csv"
    sunday_output_file = f"{PROJECT_SOURCE_FILES_DIR}/metro_data/sunday_ridership_with_trip_length.csv"
    late_night_output_file = f"{PROJECT_SOURCE_FILES_DIR}/metro_data/late_night_ridership_with_trip_length.csv"

    # read the input csv files
    weekday = pd.read_csv(weekday_input_file)
    saturday = pd.read_csv(saturday_input_file)
    sunday = pd.read_csv(sunday_input_file)
    late_night = pd.read_csv(late_night_input_file)
    stations = pd.read_csv(station_input_file)

    # # station name mismatch cleaning
    # station_names = set(stations['station_name'].unique())
    # weekday_stations = set(weekday['ent_station'].unique()).union(set(weekday['ext_station'].unique()))

    # unmatched_stations = weekday_stations - station_names
    # print(sorted(unmatched_stations))
    # print(sorted(station_names))

    # replace station names with the mapped ones
    corrections = load_station_name_corrections(path_to_name_corrections_csv)

    stations['station_name'] = stations['station_name'].apply(lambda x: normalize_and_correct_name(x, corrections))

    weekday['ent_station'] = weekday['ent_station'].apply(lambda x: normalize_and_correct_name(x, corrections))
    weekday['ext_station'] = weekday['ext_station'].apply(lambda x: normalize_and_correct_name(x, corrections))

    saturday['ent_station'] = saturday['ent_station'].apply(lambda x: normalize_and_correct_name(x, corrections))
    saturday['ext_station'] = saturday['ext_station'].apply(lambda x: normalize_and_correct_name(x, corrections))

    sunday['ent_station'] = sunday['ent_station'].apply(lambda x: normalize_and_correct_name(x, corrections))
    sunday['ext_station'] = sunday['ext_station'].apply(lambda x: normalize_and_correct_name(x, corrections))

    late_night['ent_station'] = late_night['ent_station'].apply(lambda x: normalize_and_correct_name(x, corrections))
    late_night['ext_station'] = late_night['ext_station'].apply(lambda x: normalize_and_correct_name(x, corrections))

    # stations per metroline
    red_stations = stations[stations['metroline'] == 'red']['station_name'].to_list()
    green_stations = stations[stations['metroline'] == 'green']['station_name'].to_list()
    orange_stations = stations[stations['metroline'] == 'orange']['station_name'].to_list()
    blue_stations = stations[stations['metroline'] == 'blue']['station_name'].to_list()
    silver_stations = stations[stations['metroline'] == 'silver']['station_name'].to_list()
    yellow_stations = stations[stations['metroline'] == 'yellow']['station_name'].to_list()

    metro_lines = [
        red_stations,
        green_stations,
        orange_stations,
        blue_stations,
        silver_stations,
        yellow_stations
    ]

    # create the Graph
    G = nx.Graph()
    for line_stations in metro_lines:
        for i in range(len(line_stations) - 1):
            G.add_edge(line_stations[i], line_stations[i + 1])

    for _, row in stations.iterrows():
        G.nodes[row["station_name"]]["lat"] = row["lat"]
        G.nodes[row["station_name"]]["lon"] = row["lon"]
        G.nodes[row["station_name"]]["line"] = row["metroline"]

    # save the Graph
    with open(f"{PROJECT_TRANSFORMED_FILES_DIR}/dc_metro_graph.pickle", "wb") as f:
        pickle.dump(G, f)

    def get_trip_length(graph, ent_station, ext_station):
        """
        Get the shortest path length (number of stations) between two stations.
        
        Parameters:
        - graph (nx.Graph): The metro graph.
        - ent_station (str): Entry station.
        - ext_station (str): Exit station.
        
        Returns:
        - int: Number of stations in the shortest path.
        """
        try:
            return nx.shortest_path_length(graph, source=ent_station, target=ext_station)
        except nx.NetworkXNoPath:
            return None

    # add trip length to each trip, based on the graph
    weekday['trip_length'] = weekday.apply(
        lambda row: get_trip_length(G, row['ent_station'], row['ext_station']),
        axis=1
    )
    saturday['trip_length'] = saturday.apply(
        lambda row: get_trip_length(G, row['ent_station'], row['ext_station']),
        axis=1
    )
    sunday['trip_length'] = sunday.apply(
        lambda row: get_trip_length(G, row['ent_station'], row['ext_station']),
        axis=1
    )
    late_night['trip_length'] = late_night.apply(
        lambda row: get_trip_length(G, row['ent_station'], row['ext_station']),
        axis=1
    )

    # output df
    weekday.to_csv(weekday_output_file, index=False)
    saturday.to_csv(saturday_output_file, index=False)
    sunday.to_csv(sunday_output_file, index=False)
    late_night.to_csv(late_night_output_file, index=False)

    print("Attempting to push csv files to S3")
    try:
        s3_client.upload_file(weekday_output_file, S3_BUCKET, f"metro/raw/weekday_ridership.csv")
        s3_client.upload_file(saturday_output_file, S3_BUCKET, f"metro/raw/saturday_ridership.csv")
        s3_client.upload_file(sunday_output_file, S3_BUCKET, f"metro/raw/sunday_ridership.csv")
        s3_client.upload_file(late_night_output_file, S3_BUCKET, f"metro/raw/late_night_ridership.csv")
        print("Finished pushing csv files to S3")
    except Exception as e:
        print(f"Push to S3 unsuccessful because: {e}")


if __name__ == "__main__":
    print("Main is triggered")
    s3_client = boto3.client("s3")  # Create client for manual execution
    add_shortest_trip_length(s3_client)
