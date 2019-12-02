from flask import Flask, render_template, Blueprint, request, redirect, jsonify
from app.database import db
from sqlalchemy import create_engine
from .forms import homeFilterForm
from app.programs.views import program_search_home
from app.organizations.views import organization_search_home


home_blueprint = Blueprint('home', __name__, template_folder='templates')

@home_blueprint.route('/', methods=['GET', 'POST'])
@home_blueprint.route('/home', methods=['GET', 'POST'])
def home():
	print("HERE2")
	print(request.method)
	form = homeFilterForm(request.form)

	if request.method == "POST":
		print("HERE1")
		return home_search(form)

	else:
		return render_template('home.html', form=form)

def home_search(search):
	program_main_search = search.data['program_main_search']
	organizaion_main_search = search.data['organizaion_main_search']

	if program_main_search:
		if program_main_search.isdigit():
			zip_filter = program_main_search
			neighborhood_filter = ""
			program_type = search.data['select_type']
			return program_search_home(zip_filter, neighborhood_filter, program_type)
		else:
			zip_filter = ""
			neighborhood_filter = program_main_search
			program_type = search.data['select_type']
			return program_search_home(zip_filter, neighborhood_filter, program_type)

	elif organizaion_main_search:
		if organizaion_main_search.isdigit():
			zip_filter = organizaion_main_search
			neighborhood_filter = ""
			program_type = search.data['select_type']
			return organization_search_home(zip_filter, neighborhood_filter, program_type)
		else:
			zip_filter = ""
			neighborhood_filter = organizaion_main_search
			program_type = search.data['select_type']
			return organization_search_home(zip_filter, neighborhood_filter, program_type)

	else:
		zip_filter = ""
		neighborhood_filter = ""
		program_type = search.data['select_type']
		return program_search_home(zip_filter, neighborhood_filter, program_type)
