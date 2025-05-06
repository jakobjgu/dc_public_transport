# flask_api/api/routes.py

import os
import pickle
from flask import Blueprint, jsonify
from flask_cors import cross_origin
import networkx as nx
import sys
import duckdb
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from settings import (PROJECT_ROOT_DIR,PROJECT_DBT_DIR)

api_bp = Blueprint('api', __name__, url_prefix='/api')

def load_graph():
    p = os.path.join(PROJECT_ROOT_DIR, 'transformed_data', 'dc_metro_graph.pickle')
    with open(p, 'rb') as f:
        return pickle.load(f)

def load_exit_volumes():
    con = duckdb.connect(f"{PROJECT_DBT_DIR}/dev.duckdb")
    df = con.execute("SELECT * FROM mart_exit_volume_by_station_and_period").fetch_df()
    return df


@api_bp.route('/graph', methods=['GET'])
# @cross_origin()    # ← ensure CORS on this route
def get_graph():

    # Load station-usage data from duckdb
    df = load_exit_volumes()
    # pivot df so each station maps to {(day, time): value}
    pt = (
    df.pivot_table(
        index='station',
        columns=['day_type','trip_time'],
        values='average_exits',
        fill_value=0
    )
    .to_dict(orient='index')  # { station: { (day, time): value, ... }, ... }
    )

    # transform into nested { day: { time: value, ... }, ... }
    volumes = {}
    for station, dt_map in pt.items():
        nested = {}
        for (day, time), val in dt_map.items():
            nested.setdefault(day, {})[time] = val
        volumes[station] = nested

    G = load_graph()

    nodes = []
    for n, attrs in G.nodes(data=True):
        nodes.append({
            "id": n,
            "lat": attrs['lat'],
            "lon": attrs['lon'],
            "line": attrs['line'],
            "volumes": volumes.get(n, {})   # nested day → time → value
        })

    links = [
        {"source": u, "target": v, **attrs}
        for u, v, attrs in G.edges(data=True)
    ]
    return jsonify({"nodes": nodes, "links": links})
