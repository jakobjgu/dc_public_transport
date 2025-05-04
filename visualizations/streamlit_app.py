import streamlit as st
import networkx as nx
import pandas as pd
import plotly.graph_objects as go
import sys
import pickle
sys.path.append("../dc_public_transport")
from settings import PROJECT_TRANSFORMED_FILES_DIR,PROJECT_DBT_DIR
import duckdb

# Load data
@st.cache_data
def load_graph(path):
    with open(path, "rb") as f:
        G = pickle.load(f)
    return G

@st.cache_data
def load_metadata(csv_path):
    return pd.read_csv(csv_path)

@st.cache_data
def load_exit_volumes():
    con = duckdb.connect(f"{PROJECT_DBT_DIR}/dev.duckdb")
    df = con.execute("SELECT * FROM mart_exit_volume_by_station_and_period").fetch_df()
    return df


# Load files
graph = load_graph(f"{PROJECT_TRANSFORMED_FILES_DIR}/dc_metro_graph.pickle")
station_df = load_metadata(f"{PROJECT_TRANSFORMED_FILES_DIR}/dim_stations.csv")

# Sidebar filters
st.sidebar.title("Filters")
day_type = st.sidebar.selectbox("Select Day Type", options=["weekday", "saturday", "sunday", "weekday late_night"])
time_period = st.sidebar.selectbox("Select Time Period", options=["AM Peak", "Midday", "PM Peak", "Evening", "Late Night"])

# Load exit volume data
exit_df = load_exit_volumes()
exit_df["station"] = exit_df["station"].str.lower()

# Filter to current selection
filtered_exits = exit_df[
    (exit_df["day_type"] == day_type) &
    (exit_df["trip_time"] == time_period)
]

# Map: station name -> exit volume
exit_volume_map = dict(zip(filtered_exits["station"], filtered_exits["sum_exits"]))


# Map color by metro line
line_colors = {
    'red': '#be1337',  # Red
    'blue': '#0076a8',  # Blue
    'yellow': '#f4d92c',  # Yellow
    'orange': '#f7941d',  # Orange
    'green': '#00b140',  # Green
    'silver': '#a2a4a1',  # Silver
}

# Create node trace
node_x = []
node_y = []
node_text = []
node_color = []
node_size = []

for node in graph.nodes():
    data = station_df[station_df['station_name'].str.lower() == node.lower()]
    if not data.empty:
        lat = data.iloc[0]["lat"]
        lon = data.iloc[0]["lon"]
        line = data.iloc[0]["line_name"]
        node_x.append(lon)
        node_y.append(lat)
        node_text.append(node)
        node_color.append(line_colors.get(line, "gray"))
        volume = exit_volume_map.get(node.lower(), 200)
        node_size.append(volume * 0.002)  # Adjust scaling factor as needed
        graph.nodes[node]["color"] = node_color

        # - default size for nodes? Because at non-am periods there is very little traffic and nodes have no volume

# Edge traces
edge_x = []
edge_y = []
for edge in graph.edges():
    src, tgt = edge
    src_data = station_df[station_df['station_name'].str.lower() == src.lower()]
    tgt_data = station_df[station_df['station_name'].str.lower() == tgt.lower()]
    if not src_data.empty and not tgt_data.empty:
        x0, y0 = src_data.iloc[0]["lon"], src_data.iloc[0]["lat"]
        x1, y1 = tgt_data.iloc[0]["lon"], tgt_data.iloc[0]["lat"]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]

edge_trace = go.Scatter(
    x=edge_x, y=edge_y,
    line=dict(width=1, color='gray'),
    hoverinfo='none',
    mode='lines')

node_trace = go.Scatter(
    x=node_x, y=node_y,
    mode='markers+text',
    text=node_text,
    textposition="top center",
    hoverinfo='text',
    marker=dict(
        showscale=False,
        color=node_color,
        size=node_size,
        line_width=1
    )
)

# Plot layout
fig = go.Figure(data=[edge_trace, node_trace],
                layout=go.Layout(
                    title="WMATA Metro Network",
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20, l=5, r=5, t=40),
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                ))

st.plotly_chart(fig, use_container_width=True)
