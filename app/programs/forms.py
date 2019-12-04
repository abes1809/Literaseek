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

	zipcodes = [
		('60605', '60605'),
		('60610', '60610'),
		('60622', '60622'),
		('60632', '60632'),
		('60645', '60645')
	]

	open_for_public_school_enrollment = BooleanField('Open for Public School Enrollment', validators=[DataRequired()])
	select_age = SelectMultipleField('Search by program age group:', choices=age_choices)
	select_type = SelectMultipleField('Search by program type:', choices=type_choices)
	neighborhoods = SelectMultipleField('Search by neighborhoods:', choices=neighborhoods)
	zipcodes = SelectMultipleField('Search by zipcodes:', choices=zipcodes)
	search_name = StringField('Search by name:', validators=[DataRequired()])
	submit1 = SubmitField('Search')

class sendTextForm(Form):
	user_number = StringField('Your phone number', validators=[DataRequired()])
	user_email = StringField('Your email address', validators=[DataRequired()])
	program_information = StringField('program_information', validators=[DataRequired()])
	submit2 = SubmitField('Send!')
