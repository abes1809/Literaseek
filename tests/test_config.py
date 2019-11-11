# import os
# import pytest
# from config import Config, TestDevelopmentConfig

# def test_development_config(app):
#     app.config.from_object(TestDevelopmentConfig)
#     assert app.config['DEBUG']
#     assert not app.config['TESTING']
#     assert not app.config['SQLALCHEMY_TRACK_MODIFICATIONS']
#     assert app.config['SQLALCHEMY_DATABASE_URI'] == os.environ.get(
#         'DATABASE_URL')

# def test_config(app):
#     app.config.from_object(Config)
#     assert app.config['DEBUG']
#     assert app.config['TESTING']
#     assert not app.config['SQLALCHEMY_TRACK_MODIFICATIONS']
#     assert app.config['SQLALCHEMY_DATABASE_URI'] == os.environ.get(
#         'DATABASE_URL')