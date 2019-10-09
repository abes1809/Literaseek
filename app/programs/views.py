from flask import render_template, Blueprint, request, redirect
from app.models import Program, AgeGroups, program_ages
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

	print("+++++HERE+++++++++")
	print(age_groups_select)

	# programs = Program.query.filter(Program.name.like('%'+search_name+'%'), 
	# 								Program.age_groups.any(name=age_groups_select)).all()

	programs = Program.query.join(program_ages).join(AgeGroups).filter(Program.name.like('%'+search_name+'%'), AgeGroups.name.in_(age_groups_select)).all()

	# programs = Program.query.filter( 
	# 								Program.age_groups.in_(name=age_groups_select)).all()

	form = programFilterForm(request.form)
	return render_template('programs.html', programs=programs, form=form)