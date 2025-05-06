# flask_api/app.py
from flask import Flask
from flask_cors import CORS
from api.routes import api_bp

def create_app():
    app = Flask(__name__)
    CORS(app)                          # ← allow all origins
    app.register_blueprint(api_bp)
    return app

if __name__ == "__main__":
    create_app().run(debug=True)
