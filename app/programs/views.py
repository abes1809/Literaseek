from flask import render_template, Blueprint, request, redirect
from app.models import Program, Organization

programs_blueprint = Blueprint('programs', __name__, template_folder='templates')

@programs_blueprint.route('/programs', methods=['GET', 'POST'])

def programs():
	# if request.method == "POST":
	# 	return true
	# else: 
	# join = Program.query.join(Organization).join(
	# 	Organization, Program.id == League.id).

	programs = Program.query.all()

	return render_template('programs.html', programs=programs)