from flask import render_template, Blueprint, request, redirect
from .forms import directoryFilterForm

directory_blueprint = Blueprint('directory', __name__, template_folder='templates')

@directory_blueprint.route('/directory', methods=['GET', 'POST'])
def directory():
	form = directoryFilterForm(request.form)
	if request.method == 'POST':
		return search_results(form)
 
	else: 
		organization = {
			'name': '826CHI',
			'description': '826CHI is a non-profit organization dedicated to supporting students ages 6 to 18 with their creative and expository writing skills, and to helping teachers inspire their students to write. Our services are structured around the understanding that great leaps in learning can happen with one-on-one attention, and that strong writing skills are fundamental to future success.',
			'website': 'http://www.826chi.org,http://www.826chi.org',
			'phone': '3122225555'
		}
		program = {
			'name': 'AIM High',
			'presenting_organization': 'Center for Companies That Care',
			'website': 'http://www.companies-that-care.org/action,http://www.companies-that-care.org/action',
			'description': 'AIM High is a long-term, structured, college success program dedicated to dramatically improving college graduation rates among under-served youth and preparing them for careers.',
			'type': 'Workforce Development',
			'program_ages': 'Grades 9-12, Adults',
			'neighborhoods': 'Far Southwest Side, North Side, South Side, Southwest Side, West Side'
		}
		return render_template('index.html', organization=organization, program=program, form=form)

@directory_blueprint.route('/results')
def search_results(search):
	if search.data['select'] == 'Programs':
		program = {
			'name': 'AIM High',
			'presenting_organization': 'Center for Companies That Care',
			'website': 'http://www.companies-that-care.org/action,http://www.companies-that-care.org/action',
			'description': 'AIM High is a long-term, structured, college success program dedicated to dramatically improving college graduation rates among under-served youth and preparing them for careers.',
			'type': 'Workforce Development',
			'program_ages': 'Grades 9-12, Adults',
			'neighborhoods': 'Far Southwest Side, North Side, South Side, Southwest Side, West Side'
		}
		organization = {}
	elif search.data['select'] == 'Organizations':
		organization = {
			'name': '826CHI',
			'description': '826CHI is a non-profit organization dedicated to supporting students ages 6 to 18 with their creative and expository writing skills, and to helping teachers inspire their students to write. Our services are structured around the understanding that great leaps in learning can happen with one-on-one attention, and that strong writing skills are fundamental to future success.',
			'website': 'http://www.826chi.org,http://www.826chi.org',
			'phone': '3122225555'
		}
		program = {}
    # if not results:
    #     flash('No results found!')
    #     return redirect('/')

    # else:
    #     # display results
	form = directoryFilterForm(request.form)
	return render_template('index.html', organization=organization, program=program, form=form)