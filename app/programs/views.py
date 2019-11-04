from flask import render_template, Blueprint, request, redirect, session
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
		# neighborhoods = get_neighborhoods()
		programs = Program.query.join(neighborhood_programs).join(Regions).join(Neighborhoods).all()

		return render_template('programs.html', programs=programs, form=form)

@programs_blueprint.route('/org_search')
def program_search(search):
	conditions = identify_filters(search)

	all_programs = Program.query.join(program_ages).join(program_types).join(AgeGroups).join(ProgramType).join(neighborhood_programs).join(Regions).join(Neighborhoods).filter(*conditions).all()

	form = programFilterForm(request.form)
	return render_template('programs.html', programs=all_programs, form=form)


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

def get_neighborhoods():
	engine = create_engine(db)
	connection = engine.connect()

	my_query = 'SELECT * FROM neighborhoods'
	results = connection.execute(my_query).fetchall()

	return results