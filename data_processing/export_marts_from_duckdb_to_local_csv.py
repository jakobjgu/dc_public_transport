import duckdb
import sys
sys.path.append("../dc_metro")
from settings import PROJECT_TRANSFORMED_FILES_DIR

mart_dim_stations_query = f"""
COPY (SELECT * FROM dim_stations)
TO '{PROJECT_TRANSFORMED_FILES_DIR}/dim_stations.csv'
(FORMAT CSV);
"""

with duckdb.connect("metro_analytics_dbt/dev.duckdb") as con:
    con.execute(mart_dim_stations_query)