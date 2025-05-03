import os
from dotenv import load_dotenv, find_dotenv

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

S3_BUCKET=os.getenv("S3_BUCKET")
S3_STATION_LINE_MAP_PATH=os.getenv("S3_STATION_LINE_MAP_PATH")
PROJECT_SOURCE_FILES_DIR=os.getenv("PROJECT_SOURCE_FILES_DIR")
PROJECT_TRANSFORMED_FILES_DIR=os.getenv("PROJECT_TRANSFORMED_FILES_DIR")
PROJECT_DBT_DIR=os.getenv("PROJECT_DBT_DIR")
WMATA_DEMO_API_KEY=os.getenv("WMATA_DEMO_API_KEY")