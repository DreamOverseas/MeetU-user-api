from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from config import Config
from extensions import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)
    db.init_app(app)
    api = Api(app)

    # Import and initialize routes here to avoid circular imports
    from routes import initialize_routes
    initialize_routes(api)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
