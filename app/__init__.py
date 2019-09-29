from flask import Flask
import os
from flask import render_template
from config import Config

from app.database import db
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from app.directory.views import directory_blueprint
from app.home.views import home_blueprint

import pymysql
pymysql.install_as_MySQLdb()

migrate = Migrate()

def create_app():
	app = Flask(__name__,  instance_relative_config=False)
	app.config.from_object(Config)

	db.init_app(app)
	migrate.init_app(app, db)

	app.register_blueprint(directory_blueprint)
	app.register_blueprint(home_blueprint)

	return app