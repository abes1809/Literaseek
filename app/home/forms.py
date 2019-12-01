from wtforms import Form, SelectField, SubmitField, StringField, BooleanField
from wtforms.validators import DataRequired
from markupsafe import Markup

class homeFilterForm(Form):
	type_choices = [
		('Pre-Reading', 'Pre-Reading'),
		('Pre-Writing', 'Pre-Writing'),
		('Writing', 'Writing'),
		('Reading', 'Reading'),
		('Expository Writing', 'Expository Writing'),
		('Creative Writing', 'Creative Writing'),
		('Dramatic Play', 'Dramatic Play'),
		('Book Access & Distribution', 'Book Access & Distribution'),
		('ELL/ESL', 'ELL/ESL'),
		('GED Prep', 'GED Prep'),
		('Workforce Development', 'Workforce Development'),
		('Teacher Training', 'Teacher Training'),
		('Curriculum Development', 'Cirriculum Development'),
		('Other', 'Other'),
	]

	program_main_search = StringField('Search By Zipcode or Neighborhood:', validators=[DataRequired()])
	organizaion_main_search = StringField('Search By Zipcode, Neighborhood, or Name:', validators=[DataRequired()])
	select_type = SelectField('Search by Program Type:', choices=type_choices)
	submit = SubmitField('Enter Search')