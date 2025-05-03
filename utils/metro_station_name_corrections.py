import pandas as pd
import sys
sys.path.append("../dc_public_transport")
sys.path.append("../dc_public_transport/data_processing")
from settings import (
    PROJECT_SOURCE_FILES_DIR
    )

# Load the corrections CSV
def load_station_name_corrections(path_to_csv):
    df = pd.read_csv(path_to_csv)
    return dict(zip(df["original_name"], df["corrected_name"]))

# Combined normalization and correction function
def normalize_and_correct_name(name, corrections_dict):
    if pd.isnull(name):
        return name
    corrected = corrections_dict.get(name, name)
    name = corrected.strip().replace("–", " ").replace("—", " ").lower()
    return name.lower()

# Optional: small test or demo when running directly
if __name__ == "__main__":
    try:
        # Define directory paths
        path_to_csv = f"{PROJECT_SOURCE_FILES_DIR}/metro_data/station_name_corrections.csv"
        corrections = load_station_name_corrections(path_to_csv)
        test_names = ["College Park-U of Md",
                      "King St-Old Town",
                      "Brookland",
                      "Archives-Navy Memorial",
                      "Ballston",
                      " Foggy Bottom–GWU "]
        for name in test_names:
            print(f"{name} -> {normalize_and_correct_name(name, corrections)}")
    except Exception as e:
        print(f"Error during test: {e}")
