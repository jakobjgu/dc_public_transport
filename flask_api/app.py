# flask_api/app.py
from flask import Flask
from flask_cors import CORS
from api.routes import api_bp

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    app.register_blueprint(api_bp)
    return app

if __name__ == "__main__":
    app = create_app()
    print(app.url_map)  # sanity-check registered routes
    app.run(host="0.0.0.0", port=5000, debug=False)
