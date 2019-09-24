from flask import render_template, Blueprint, request, redirect

home_blueprint = Blueprint('home', __name__, template_folder='templates')

@home_blueprint.route('/')
@home_blueprint.route('/home')
def home():
	return render_template('home.html')