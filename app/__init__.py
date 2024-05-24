import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# app.secret_key = "this-is-my-secret-key"

app.config["APPDATA_PATH"] = f"{os.path.abspath(os.path.dirname(__file__) + '/../data')}"

# Database
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{app.config['APPDATA_PATH']}/database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)

from app.models.db_model import create_tables
create_tables()

from app.controllers import routes
