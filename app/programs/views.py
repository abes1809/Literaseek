from flask import render_template, Blueprint, request, redirect
from app.models import Program, AgeGroups, ProgramType, program_ages, program_types
from .forms import programFilterForm

programs_blueprint = Blueprint('programs', __name__, template_folder='templates')

@programs_blueprint.route('/programs', methods=['GET', 'POST'])
def programs():
	form = programFilterForm(request.form)

	if request.method == "POST":
		return program_search(form)

	else:
		programs = Program.query.all()

		return render_template('programs.html', programs=programs, form=form)

@programs_blueprint.route('/org_search')
def program_search(search):
	search_name = search.data['search_name']
	age_groups_select = search.data['select_age']
	type_select = search.data['select_type']
	open_for_public_school_enrollment = search.data['open_for_public_school_enrollment']

	programs = Program.query.join(program_ages).join(program_types).join(AgeGroups).join(ProgramType).filter(
		Program.name.like('%'+search_name+'%'), 
		AgeGroups.name.in_(age_groups_select),
		ProgramType.name.in_(type_select)).all()

	form = programFilterForm(request.form)
	return render_template('programs.html', programs=programs, form=form)


# def identify_filters(search_name, age_groups_select, type_select, open_for_public_school_enrollment, programs):
# 	if search_name: 
# 		name_filter = Program.name.like('%'+search_name+'%')