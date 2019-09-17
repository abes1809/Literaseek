from wtforms import Form, SelectField, SubmitField

class directoryFilterForm(Form):
	choices = [
	('Programs', 'Programs'),
	('Organizations', 'Organizations')
	]
	select = SelectField('Filter by Program or Organization:', choices=choices)
	submit = SubmitField('Filter')

