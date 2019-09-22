from flask import current_app
from flask import render_template

@current_app.route('/')
@current_app.route('/home')
def home():
	return render_template('home.html', title='Home')