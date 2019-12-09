from wtforms import Form, SelectField, SubmitField, StringField, BooleanField
from wtforms.validators import DataRequired

class homeFilterForm(Form):
	type_choices = [
		('', ''),
		('Pre-Reading', 'Pre-Reading'),
		('Pre-Writing', 'Pre-Writing'),
		('Writing', 'Writing'),
		('Reading', 'Reading'),
		('Expository Writing', 'Expository Writing'),
		('Create Writing', 'Creative Writing'),
		('Dramatic Play', 'Dramatic Play'),
		('Book Access & Distribution', 'Book Access & Distribution'),
		('ELL/ESL', 'ELL/ESL'),
		('GED Prep', 'GED Prep'),
		('Workforce Development', 'Workforce Development'),
		('Teacher Training', 'Teacher Training'),
		('Curriculum Development', 'Cirriculum Development'),
		('Other', 'Other'),
	]

	program_main_search = StringField('Search by Zipcode or Neighborhood:', validators=[DataRequired()])
	organizaion_main_search = StringField('Search by Zipcode or Neighborhood:', validators=[DataRequired()])
	select_type = SelectField('Search by Program Type:', choices=type_choices)
	submit = SubmitField('Enter Search')