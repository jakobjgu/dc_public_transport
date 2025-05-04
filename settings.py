import os
from dotenv import load_dotenv, find_dotenv

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

if os.getenv('ENV') == 'EC2':
    base_path = os.getenv('EC2_BASE_PATH')
else:
    base_path = os.getenv('LOCAL_BASE_PATH')

# Expand the ~ to the full home directory path
base_path = os.path.expanduser(base_path)

S3_BUCKET=os.getenv("S3_BUCKET")
S3_STATION_LINE_MAP_PATH=os.getenv("S3_STATION_LINE_MAP_PATH")
WMATA_DEMO_API_KEY=os.getenv("WMATA_DEMO_API_KEY")

# paths
PROJECT_SOURCE_FILES_BASE_DIR=os.getenv("PROJECT_SOURCE_FILES_BASE_DIR")
PROJECT_TRANSFORMED_FILES_BASE_DIR=os.getenv("PROJECT_TRANSFORMED_FILES_BASE_DIR")
PROJECT_DBT_BASE_DIR=os.getenv("PROJECT_DBT_BASE_DIR")

PROJECT_SOURCE_FILESDIR=base_path + PROJECT_SOURCE_FILES_BASE_DIR
PROJECT_TRANSFORMED_FILES_DIR=base_path + PROJECT_TRANSFORMED_FILES_BASE_DIR
PROJECT_DBT_DIR=base_path + PROJECT_DBT_BASE_DIR