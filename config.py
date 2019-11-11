import os

class Config:

	TESTING = os.environ.get('TESTING')
	DEBUG = os.environ.get('DEBUG')
	SQLALCHEMY_DATABASE_URI =  os.environ.get('SQLALCHEMY_DATABASE_URI')
	SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
	MAPBOX_TOKEN = os.environ.get('MAPBOX_TOKEN')