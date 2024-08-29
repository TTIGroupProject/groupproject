from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_marshmallow import Marshmallow
import os
from dotenv import load_dotenv
from models import db
import pyodbc
from env import connection

load_dotenv()

ma = Marshmallow()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("MYSQL_DATABASE_URI")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
    app.config['UPLOAD_FOLDER'] = os.getenv("UPLOAD_FOLDER")
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max file size

    db.init_app(app)
    ma.init_app(app)
    jwt = JWTManager(app)

    CORS(app, resources={r"/*": {"origins": "*"}})

    from routes import customer_bp, provider_bp, review_bp, service_bp, booking_bp

    app.register_blueprint(customer_bp, url_prefix='/api/customer')
    app.register_blueprint(provider_bp, url_prefix='/api/provider')
    app.register_blueprint(review_bp, url_prefix='/api/review')
    app.register_blueprint(service_bp, url_prefix='/api/service')
    app.register_blueprint(booking_bp, url_prefix='/api/booking')

    return app

app = create_app()
with app.app_context():
    db.create_all()  # Creates database tables based on the defined models

# This line should be removed or commented out for production.
# app.run(port=5000)