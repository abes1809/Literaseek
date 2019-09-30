from wtforms import Form, SelectField, SubmitField, StringField
from wtforms.validators import DataRequired

class organizationFilterForm(Form):
	# choices = [
	# ('Programs', 'Programs'),
	# ('Organizations', 'Organizations')
	# ]
	# select = SelectField('Filter by Program or Organization:', choices=choices)
	search_name = StringField('Search By Name', validators=[DataRequired()])
	submit = SubmitField('Filter')