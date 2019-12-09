from flask import app, render_template, Blueprint, request, redirect, jsonify
from app.models import Organization, Program, AgeGroups, ProgramType, program_ages, program_types, neighborhood_programs, Neighborhoods, Regions, neighborhood_zips, ZipCodes
from .forms import organizationFilterForm, sendTextForm
from twilio.rest import Client
import click
import requests
import os

organizations_blueprint = Blueprint('organizations', __name__, template_folder='templates')

@organizations_blueprint.route('/organizations', methods=['GET', 'POST'])
def organizations():
	form = organizationFilterForm(request.form)

	if request.method == 'POST':
		return org_search(form)

	else:
		all_organizations = Organization.query.join(Program).join(program_ages).join(program_types).join(AgeGroups).join(ProgramType).join(neighborhood_programs).join(Regions).join(Neighborhoods).join(neighborhood_zips).join(ZipCodes).order_by(Organization.name)

		return render_template('organizations.html', organizations=all_organizations, form=form)

@organizations_blueprint.route('/organization_view/<organization_id>', methods=['GET', 'POST'])
def organization_view(organization_id):

	organizations = Organization.query.join(Program).join(program_ages).join(program_types).join(AgeGroups).join(ProgramType).join(neighborhood_programs).join(Regions).join(Neighborhoods).join(neighborhood_zips).join(ZipCodes).filter(Organization.id == organization_id).order_by(Organization.name).all()

	info_opening = "Hello! Below you will find the information for " +  organizations[0].name + "."
	info_phone = " Organization Phone Number: " + organizations[0].phone
	info_website= " Organization Website: " + organizations[0].website
	info_address =  " Organization Address: " + organizations[0].address
	organization_information = (
		info_opening + 
		info_phone +
		info_website + 
		info_address
	)
	
	form = sendTextForm(request.form, organization_information=organization_information)

	if form.data['user_number']:
		sendText(form)
	elif form.data['user_email']:
		sendEmail(form)

	return render_template('organization_view.html', organizations=organizations, form=form)


@organizations_blueprint.route('/org_search')
def org_search(search):
	conditions = identify_filters(search)

	organizations = Organization.query.join(Program).join(program_ages).join(program_types).join(AgeGroups).join(ProgramType).join(neighborhood_programs).join(Regions).join(Neighborhoods).join(neighborhood_zips).join(ZipCodes).filter(*conditions).all()

	form = organizationFilterForm(request.form)

	return render_template('organizations.html', organizations=organizations, form=form)

@organizations_blueprint.route('/organization_search_home', methods=['GET', 'POST'])
def organization_search_home(zip_filter, neighborhood_filter, program_type):
	conditions = identify_filters_home(zip_filter, neighborhood_filter, program_type)

	organizations = Organization.query.join(Program).join(program_ages).join(program_types).join(AgeGroups).join(ProgramType).join(neighborhood_programs).join(Regions).join(Neighborhoods).join(neighborhood_zips).join(ZipCodes).filter(*conditions).all()

	form = organizationFilterForm(request.form)

	return render_template('organizations.html', organizations=organizations, form=form)

@organizations_blueprint.route('/organization_data', methods=['GET', 'POST'])
def organization_data():
	org_ids = request.args.getlist('ids[]')
	
	organizations = Organization.query.filter(Organization.id.in_(org_ids)).all()

	organizations = jsonify([organization.to_dict() for organization in organizations])

	return organizations

def identify_filters(search):
	search_name = search.data['search_name']
	age_groups_select = search.data['select_age']
	type_select = search.data['select_type']
	search_neighborhoods =  search.data["neighborhoods"]
	search_zips =  search.data["zipcodes"]

	conditions = []

	if search_name: 
		conditions.append(Organization.name.like('%'+search_name+'%'))

	if age_groups_select:
		conditions.append(AgeGroups.name.in_(age_groups_select))

	if type_select:
		conditions.append(ProgramType.name.in_(type_select))

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
