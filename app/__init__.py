from flask import Flask
import os
# from config import Config

app = Flask(__name__, instance_relative_config=True)
# app.config.from_object(Config)

from app.directory.views import directory_blueprint

app.register_blueprint(directory_blueprint)

from app import home