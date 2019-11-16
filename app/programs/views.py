from flask import Flask, render_template, Blueprint, request, redirect, jsonify
from app.database import db
from sqlalchemy import create_engine
from app.models import Program, AgeGroups, ProgramType, program_ages, program_types, neighborhood_programs, Neighborhoods, Regions
from .forms import programFilterForm

programs_blueprint = Blueprint('programs', __name__, template_folder='templates')

@programs_blueprint.route('/programs', methods=['GET', 'POST'])
def programs():
	form = programFilterForm(request.form)

	if request.method == "POST":
		return program_search(form)

	else:
		programs = Program.query.join(neighborhood_programs).join(Regions).join(Neighborhoods).all()

		return render_template('programs.html', programs=programs, form=form)

@programs_blueprint.route('/org_search')
def program_search(search):
	conditions = identify_filters(search)

	all_programs = Program.query.join(program_ages).join(program_types).join(AgeGroups).join(ProgramType).join(neighborhood_programs).join(Regions).join(Neighborhoods).filter(*conditions).all()

	form = programFilterForm(request.form)
	return render_template('programs.html', programs=all_programs, form=form)


@programs_blueprint.route('/neighborhoods', methods=['GET'])
def neighborhoods():

	all_neighborhoods = Neighborhoods.query.all()

	all_neighborhoods = jsonify([neiborhood.to_dict() for neiborhood in all_neighborhoods])

	return all_neighborhoods

@programs_blueprint.route('/program_regions/<program_name>', methods=['GET'])
def program_regions(program_name):
	data = Program.query.filter(Program.name == program_name).all()
	program_regions = jsonify([neiborhood.to_dict() for neiborhood in data])


	return program_regions


def identify_filters(search):
	search_name = search.data['search_name']
	age_groups_select = search.data['select_age']
	type_select = search.data['select_type']
	open_for_public_school_enrollment = search.data['open_for_public_school_enrollment']
	search_neighborhoods =  search.data["neighborhoods"]

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

	return conditions