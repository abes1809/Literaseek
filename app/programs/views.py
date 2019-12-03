from flask import Flask, render_template, Blueprint, request, redirect, jsonify
from app.database import db
from sqlalchemy import create_engine
from app.models import Program, AgeGroups, ProgramType, program_ages, program_types, neighborhood_programs, Neighborhoods, Regions, neighborhood_zips, ZipCodes
from .forms import programFilterForm, sendTextForm
from twilio.rest import Client
import requests
import os

programs_blueprint = Blueprint('programs', __name__, template_folder='templates')

@programs_blueprint.route('/programs', methods=['GET', 'POST'])
def programs():
	form = programFilterForm(request.form)

	if request.method == "POST":
		return program_search(form)

	else:
		programs = Program.query.join(neighborhood_programs).join(Regions).join(Neighborhoods).all()

		return render_template('programs.html', programs=programs, form=form)

@programs_blueprint.route('/program_search', methods=['GET', 'POST'])
def program_search(search):
	conditions = identify_filters(search)

	all_programs = Program.query.join(program_ages).join(program_types).join(AgeGroups).join(ProgramType).join(neighborhood_programs).join(Regions).join(Neighborhoods).join(neighborhood_zips).join(ZipCodes).filter(*conditions).all()

	form = programFilterForm(request.form)
	return render_template('programs.html', programs=all_programs, form=form)


@programs_blueprint.route('/program_search_home', methods=['GET', 'POST'])
def program_search_home(zip_filter, neighborhood_filter, program_type):
	conditions = identify_filters_home(zip_filter, neighborhood_filter, program_type)

	all_programs = Program.query.join(program_ages).join(program_types).join(AgeGroups).join(ProgramType).join(neighborhood_programs).join(Regions).join(Neighborhoods).join(neighborhood_zips).join(ZipCodes).filter(*conditions).all()

	form = programFilterForm(request.form)

	return render_template('programs.html', programs=all_programs, form=form)

@programs_blueprint.route('/program_view/<program_id>', methods=['GET', 'POST'])
def program_view(program_id):

	programs = Program.query.join(program_ages).join(program_types).join(AgeGroups).join(ProgramType).join(neighborhood_programs).join(Regions).join(Neighborhoods).filter(Program.id == program_id).all()

	info_opening = "Hello! Below you will find the information for " +  programs[0].name + "."
	info_phone = " Organization Phone Number: " + programs[0].organizations.phone
	info_website= " Program Website: " + programs[0].website
	info_address =  " Organization Address: " + programs[0].organizations.address
	program_information = (
		info_opening + 
		info_phone +
		info_website + 
		info_address
	)
	
	form = sendTextForm(request.form, program_information=program_information)

	if form.data['user_number']:
		sendText(form)
	elif form.data['user_email']:
		sendEmail(form)

	return render_template('program_view.html', programs=programs, form=form)


@programs_blueprint.route('/neighborhoods', methods=['GET'])
def neighborhoods():

	all_neighborhoods = Neighborhoods.query.all()

	all_neighborhoods = jsonify([neiborhood.to_dict() for neiborhood in all_neighborhoods])

	return all_neighborhoods

@programs_blueprint.route('/program_regions/<program_name>', methods=['GET'])
def program_regions(program_name):
	form = programFilterForm(request.form)
	data = Program.query.filter(Program.name == program_name).all()
	program_regions = jsonify([neiborhood.to_dict() for neiborhood in data])


	return program_regions

def sendText(form):
	user_number = form.data['user_number']
	program_information = form.data['program_information']

	account_sid = os.environ.get('TWILLIOACCOUNTSID')
	auth_token = os.environ.get('TWILLIOAUTHTOKEN')
	from_phone = os.environ.get('TWILLIONUMBER')

	client = Client(account_sid, auth_token)

	message = client.messages \
	                .create(
	                     body=program_information,
	                     from_=from_phone,
	                     to='+1 ' + user_number
	                 )

def sendEmail(form):
	user_email = form.data['user_email']
	program_information = form.data['program_information']

	domain = os.environ.get('MAILGUNDOMAIN')
	api_key = os.environ.get('MAILGUNAPI')
	request_url = "https://api.mailgun.net/v3/" + domain + "/messages"

	response = requests.post(
	        request_url,
	        auth=("api", api_key),
	        data={"from": "Literaseek <mailgun@" + domain + ">",
	              "to": user_email,
	              "subject": "Hello",
	              "text": program_information})

	print(response.text)
	return response.text

def identify_filters(search):
	search_name = search.data['search_name']
	age_groups_select = search.data['select_age']
	type_select = search.data['select_type']
	open_for_public_school_enrollment = search.data['open_for_public_school_enrollment']
	search_neighborhoods =  search.data["neighborhoods"]
	search_zips =  search.data["zipcodes"]

	conditions = []

	if search_name: 
		conditions.append(Program.name.like('%'+search_name+'%'))

	if age_groups_select:
		conditions.append(AgeGroups.name.in_(age_groups_select))

	if type_select:
		conditions.append(ProgramType.name.in_(type_select))

	if open_for_public_school_enrollment:
		conditions.append(Program.open_public_school_enrollement.is_(open_for_public_school_enrollment))

	if search_neighborhoods:
		conditions.append(Regions.name.in_(search_neighborhoods))

	if search_zips:
		conditions.append(ZipCodes.name.in_(search_zips))

	return conditions

def identify_filters_home(search_zips, search_neighborhoods, type_select):

	conditions = []

	if type_select:
		conditions.append(ProgramType.name.like(type_select))

	if search_neighborhoods:
		conditions.append(Neighborhoods.name.like('%'+search_neighborhoods+'%'))

	if search_zips:
		conditions.append(ZipCodes.name.like('%'+search_zips+'%'))

	return conditions

