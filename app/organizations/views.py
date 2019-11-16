from flask import render_template, Blueprint, request, redirect, jsonify
from app.models import Organization, Program, AgeGroups, ProgramType, program_ages, program_types, neighborhood_programs, Neighborhoods, Regions
from .forms import organizationFilterForm

organizations_blueprint = Blueprint('organizations', __name__, template_folder='templates')

@organizations_blueprint.route('/organizations', methods=['GET', 'POST'])

def organizations():
	form = organizationFilterForm(request.form)

	if request.method == 'POST':
		return org_search(form)

	else:
		all_organizations = Organization.query.all()

		return render_template('organizations.html', organizations=all_organizations, form=form)


@organizations_blueprint.route('/org_search')
def org_search(search):
	conditions = identify_filters(search)

	organizations = Organization.query.join(Program).join(program_ages).join(program_types).join(AgeGroups).join(ProgramType).join(neighborhood_programs).join(Regions).join(Neighborhoods).filter(*conditions).all()

	form = organizationFilterForm(request.form)

	return render_template('organizations.html', organizations=organizations, form=form)


# @organizations_blueprint.route('/organization_data')
# def organization_data(organizations):

# 	organization_locations = jsonify([organization.to_dict() for organization in organizations])

# 	return organization_locations



def identify_filters(search):
	search_name = search.data['search_name']
	age_groups_select = search.data['select_age']
	type_select = search.data['select_type']
	search_neighborhoods =  search.data["neighborhoods"]

	conditions = []

	if search_name: 
		conditions.append(Organization.name.like('%'+search_name+'%'))

	if age_groups_select:
		conditions.append(AgeGroups.name.in_(age_groups_select))

	if type_select:
		conditions.append(ProgramType.name.in_(type_select))

	if search_neighborhoods:
		conditions.append(Regions.name.in_(search_neighborhoods))

	return conditions