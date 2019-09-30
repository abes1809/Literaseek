from wtforms import Form, SelectMultipleField, SubmitField, StringField
from wtforms.validators import DataRequired

class programFilterForm(Form):
	age_choices = [
		('PreK (Age 0-3)', 'PreK (Age 0-3)'),
		('PreK (Age 3-5)', 'PreK (Age 3-5)'),
		('Grades K-8', 'Grades K-8'),
		('Grades 9-12', 'Grades 9-12'),
		('Adult', 'Adult'),
	]
	select_age = SelectMultipleField('Filter by Program or Organization:', choices=age_choices)
	search_name = StringField('Search By Name', validators=[DataRequired()])
	submit = SubmitField('Filter')