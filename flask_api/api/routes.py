# flask_api/api/routes.py

import os
import pickle
from flask import Blueprint, jsonify
import networkx as nx
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from settings import PROJECT_ROOT_DIR

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/ridership', methods=['GET'])
def get_ridership():
    # Build the full path to your pickle
    pkl_path = os.path.join(PROJECT_ROOT_DIR, 'transformed_data', 'dc_metro_graph.pickle')

    # Load the graph
    with open(pkl_path, 'rb') as f:
        graph: nx.Graph = pickle.load(f)

    # Serialize edges to JSON-friendly format
    data = []
    for u, v, attrs in graph.edges(data=True):
        record = {
            "from": u,
            "to": v,
            **attrs  # include any edge attributes
        }
        data.append(record)

    return jsonify(data)
