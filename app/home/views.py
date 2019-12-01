from flask import render_template, Blueprint, request, redirect, url_for
from .forms import homeFilterForm 

home_blueprint = Blueprint('home', __name__, template_folder='templates')

@home_blueprint.route('/')
@home_blueprint.route('/home')
def home():
	form = homeFilterForm(request.form)

	if request.method == "POST":
		return search(form)

	else:
		return render_template('home.html', form=form)

def search(search):
	program_main_search = search.data['program_main_search']

	if program_main_search:
		return redirect(url_for('app.programs.program_search', search=search))