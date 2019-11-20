from wtforms import Form, SelectMultipleField, SubmitField, StringField, BooleanField
from wtforms.validators import DataRequired

class programFilterForm(Form):
	age_choices = [
		('PreK (Age 0-3)', 'PreK (Age 0-3)'),
		('PreK (Age 3-5)', 'PreK (Age 3-5)'),
		('Grades K-8', 'Grades K-8'),
		('Grades 9-12', 'Grades 9-12'),
		('Adult', 'Adult'),
	]

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
		('Cirriculum Development', 'Cirriculum Development'),
		('Other', 'Other'),
	]

	neighborhoods = [
		('South Side', 'Bridgeport'),
		('South Side', 'Chinatown'),
		('North Side', 'Lakeview'),
		('Far North Side', 'Rogers Park'),
		('West Side', 'United Center'),
		('South Side', 'Armour Square'),
		('Far Southwest Side', 'Avalon Park'),
	]

	open_for_public_school_enrollment = BooleanField('Open for Public School Enrollment', validators=[DataRequired()])
	select_age = SelectMultipleField('Filter by program age group:', choices=age_choices)
	select_type = SelectMultipleField('Filter by program type:', choices=type_choices)
	neighborhoods = SelectMultipleField('Filter by neighborhoods:', choices=neighborhoods)
	search_name = StringField('Search By Name', validators=[DataRequired()])
	submit1 = SubmitField('Filter')

class sendTextForm(Form):
	user_number = StringField('Your phone number', validators=[DataRequired()])
	user_email = StringField('Your email address', validators=[DataRequired()])
	program_information = StringField('program_information', validators=[DataRequired()])
	submit2 = SubmitField('Send!')