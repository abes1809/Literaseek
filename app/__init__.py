from flask import Flask
import os
from flask import render_template
from config import Config

from app.database import db
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from app.organizations.views import organizations_blueprint
from app.programs.views import programs_blueprint
from app.home.views import home_blueprint

import pymysql
pymysql.install_as_MySQLdb()

migrate = Migrate()

_static_folder = os.path.abspath("static/")

def create_app():
	app = Flask(__name__,  instance_relative_config=False)
	app.config.from_object(Config)

	with app.app_context():

		db.init_app(app)
		migrate.init_app(app, db)

		app.register_blueprint(home_blueprint)
		app.register_blueprint(programs_blueprint)
		app.register_blueprint(organizations_blueprint)

	return app