from flask import Flask
import os
from flask import render_template
# from config import Config

# app.config.from_object(Config)
from app.directory.views import directory_blueprint
from app.home.views import home_blueprint

def create_app():
	app = Flask(__name__, instance_relative_config=True)
	app.register_blueprint(directory_blueprint)
	app.register_blueprint(home_blueprint)
	return app