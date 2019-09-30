from flask import render_template, Blueprint, request, redirect
from app.models import Organization
from .forms import organizationFilterForm

organizations_blueprint = Blueprint('organizations', __name__, template_folder='templates')

@organizations_blueprint.route('/organizations', methods=['GET', 'POST'])

def organizations():
	form = organizationFilterForm(request.form)

	if request.method == 'POST':
		return org_search(form)

	else:
		organizations = Organization.query.all()

		return render_template('organizations.html', organizations=organizations, form=form)


@organizations_blueprint.route('/org_search')
def org_search(search):
	search_name = search.data['search_name']
	organizations = Organization.query.filter(Organization.name.like('%'+search_name+'%')).all()

	form = organizationFilterForm(request.form)

	return render_template('organizations.html', organizations=organizations, form=form)