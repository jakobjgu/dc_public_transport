import duckdb
import subprocess
import os

# # Step 1: Export table to Parquet
# mart__ridership_enriched_query = """
# COPY (SELECT * FROM mart__ridership_enriched)
# TO 'source_files/metro_data/marts/mart__ridership_enriched.parquet'
# (FORMAT PARQUET);
# """

# parquet_path = os.path.abspath("source_files/metro_data/marts/mart__ridership_enriched.parquet")

# with duckdb.connect("metro_analytics_dbt/dev.duckdb") as con:
#     con.execute(mart__ridership_enriched_query)

# # Step 2: Upload to Snowflake stage using snowsql CLI
# mart__ridership_enriched_command = [
#     "/Applications/SnowSQL.app/Contents/MacOS/snowsql",
#     "-c", "jakob_snow",
#     "-q", f"""
#             CREATE OR REPLACE FILE FORMAT PROJECTS.RAW.parquet_format TYPE = parquet;>
#             CREATE OR REPLACE STAGE PROJECTS.RAW.mart_stage FILE_FORMAT = PROJECTS.RAW.parquet_format;>
#             PUT 'file://{parquet_path}' @PROJECTS.RAW.mart_stage;>
#             COPY INTO PROJECTS.RAW.MART__RIDERSHIP_ENRICHED FROM ( SELECT
#                 $1:ENT_STATION::varchar,
#                 $1:EXT_STATION:name::varchar,
#                 $1:ENT_TIME_PERIOD::varchar,
#                 $1:DAY_TYPE::varchar,
#                 $1:RIDERS::float,
#                 $1:TRIP_LENGTH::number
#                 FROM @PROJECTS.RAW.mart_stage);
#             """
# ]
# "The 'Copy into...' part did not work with snowsql, but using the snowflake UI this command worked:"

# """COPY INTO PROJECTS.RAW.MART__RIDERSHIP_ENRICHED
#   FROM @PROJECTS.RAW.MART_STAGE
#   FILE_FORMAT = 'parquet_format'
#   PURGE = TRUE
#   MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;"""

# # mart__ridership_enriched_result = subprocess.run(mart__ridership_enriched_command, capture_output=True, text=True)

# # # Print the CLI output
# # print("STDOUT:", mart__ridership_enriched_result.stdout)
# # print("STDERR:", mart__ridership_enriched_result.stderr)

# #############################################################
# # Step 1: Export table to Parquet
# mart__entry_volume_by_station_and_period_query = """
# COPY (SELECT * FROM mart__entry_volume_by_station_and_period)
# TO 'source_files/metro_data/marts/mart__entry_volume_by_station_and_period.parquet'
# (FORMAT PARQUET);
# """

# parquet_path = os.path.abspath("source_files/metro_data/marts/mart__entry_volume_by_station_and_period.parquet")

# with duckdb.connect("metro_analytics_dbt/dev.duckdb") as con:
#     con.execute(mart__entry_volume_by_station_and_period_query)

# # Step 2: Upload to Snowflake stage using snowsql CLI
# mart__entry_volume_by_station_and_period_command = [
#     "/Applications/SnowSQL.app/Contents/MacOS/snowsql",
#     "-c", "jakob_snow",
#     "-q", f"""
#             CREATE OR REPLACE FILE FORMAT PROJECTS.RAW.parquet_format TYPE = parquet;>
#             CREATE OR REPLACE STAGE PROJECTS.RAW.mart_stage2 FILE_FORMAT = PROJECTS.RAW.parquet_format;>
#             PUT 'file://{parquet_path}' @PROJECTS.RAW.mart_stage2;
            
#             """
# ]
# "The 'Copy into...' part did not work with snowsql, but using the snowflake UI this command worked:"

# """COPY INTO PROJECTS.RAW.MART__RIDERSHIP_ENRICHED
#   FROM @PROJECTS.RAW.MART_STAGE
#   FILE_FORMAT = 'PROJECTS.RAW.parquet_format'
#   PURGE = TRUE
#   MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;"""

# # CREATE OR REPLACE TABLE PROJECTS.RAW.mart__entry_volume_by_station_and_period (
# #                 STATION VARCHAR (90),
# #                 DAY_TYPE VARCHAR (45),
# #                 TRIP_TIME VARCHAR (45),
# #                 AVERAGE_ENTRIES FLOAT,
# #                 TRIP_COUNT NUMBER(38,0)
# #             );>
# #             COPY INTO PROJECTS.RAW.mart__entry_volume_by_station_and_period
# #             FROM @PROJECTS.RAW.MART_STAGE2
# #             FILE_FORMAT = 'PROJECTS.RAW.parquet_format'
# #             PURGE = TRUE
# #             MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE
# #             ON_ERROR = 'SKIP_FILE' 
# #             FILES = ('ROJECTS.RAW.mart__entry_volume_by_station_and_period.parquet');

# mart__entry_volume_by_station_and_period_result = subprocess.run(mart__entry_volume_by_station_and_period_command, capture_output=True, text=True)

# # Print the CLI output
# print("STDOUT:", mart__entry_volume_by_station_and_period_result.stdout)
# print("STDERR:", mart__entry_volume_by_station_and_period_result.stderr)

#############################################################
# Step 1: Export table to Parquet
mart__exit_volume_by_station_and_period_query = """
COPY (SELECT * FROM mart__entry_volume_by_station_and_period)
TO 'source_files/metro_data/marts/mart__exit_volume_by_station_and_period.parquet'
(FORMAT PARQUET);
"""

parquet_path = os.path.abspath("source_files/metro_data/marts/mart__exit_volume_by_station_and_period.parquet")

with duckdb.connect("metro_analytics_dbt/dev.duckdb") as con:
    con.execute(mart__exit_volume_by_station_and_period_query)

# Step 2: Upload to Snowflake stage using snowsql CLI
mart__exit_volume_by_station_and_period_command = [
    "/Applications/SnowSQL.app/Contents/MacOS/snowsql",
    "-c", "jakob_snow",
    "-q", f"""
            CREATE OR REPLACE FILE FORMAT PROJECTS.RAW.parquet_format TYPE = parquet;>
            CREATE OR REPLACE STAGE PROJECTS.RAW.mart_stage2 FILE_FORMAT = PROJECTS.RAW.parquet_format;>
            PUT 'file://{parquet_path}' @PROJECTS.RAW.mart_stage2;
            """
]
"The 'Copy into...' part did not work with snowsql, but using the snowflake UI this command worked:"

"""
CREATE OR REPLACE TABLE PROJECTS.RAW.mart__exit_volume_by_station_and_period (
  STATION VARCHAR (90),
  DAY_TYPE VARCHAR (45),
  TRIP_TIME VARCHAR (45),
  AVERAGE_EXITS FLOAT,
  SUM_EXITS FLOAT,
  TRIPS_TO_THIS_STATION NUMBER(38,0),
  AVERAGE_NUMBER_OF_STOPS_TO_THIS_STATION NUMBER(38,0)
);
"""

"""COPY INTO PROJECTS.RAW.mart__exit_volume_by_station_and_period
  FROM @PROJECTS.RAW.MART_STAGE
  FILE_FORMAT = 'PROJECTS.RAW.parquet_format'
  PURGE = TRUE
  MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;"""

mart__exit_volume_by_station_and_period_result = subprocess.run(mart__exit_volume_by_station_and_period_command, capture_output=True, text=True)

# Print the CLI output
print("STDOUT:", mart__exit_volume_by_station_and_period_result.stdout)
print("STDERR:", mart__exit_volume_by_station_and_period_result.stderr)