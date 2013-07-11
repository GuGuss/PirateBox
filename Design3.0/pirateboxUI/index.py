from flask import Flask, session, redirect, url_for, escape, request, render_template, render_template_string, g, request
from flaskext.babel import Babel, gettext, ngettext
import os
import codecs

app = Flask(__name__)
# This line causes an error http://stackoverflow.com/questions/12550913/flask-bable-jinja2-templates-html-syntaxerror-invalid-syntax
#app.config.from_pyfile('babel.cfg')
babel = Babel(app)

# --------- #
# FUNCTIONS #
# --------- #

# allow extension inclusion
def include_extension(extension_name):
	file_name = 'extensions/' + extension_name + '/extension.py'
	if os.path.exists(file_name):
		execfile(file_name)

# render extension template
def render_extension_template(template, **context):
	with codecs.open('extensions/' + template, 'r', encoding='utf-8') as content_file:
		content = content_file.read()
	return render_template_string(content, context=context)

# load all available extensions
# @TODO
include_extension('openstreetmap')
include_extension('helloworld')

def render_layout(content, title=None):
	return render_template('layout.html', content=content, title=title)

# ------ #
# ROUTES #
# ------ #

@app.route('/')
def index():
	return render_layout(render_template('index.html'), 'Home')

@app.route('/explore')
def explore():
	return render_layout(render_template('explore.html'), 'Explore')

@app.route('/extensions')
def extensions():
	return render_layout(render_template('extensions.html'), 'Extensions')

@app.route('/concept')
def concept():
	return render_layout(render_template('concept.html'))

@app.route('/user')
def user():
	if 'username' in session:
		return gettext(u'You are logged in')
		#Logged in as %s' % escape(session['username'])
	return gettext(u'You are NOT logged in')

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		session['username'] = request.form['username']
		return redirect(url_for('index'))
	return render_template('login.html')

@app.route('/logout')
def logout():
	# remove the username from the session if it's there
	session.pop('username', None)
	return redirect(url_for('index'))

# define the user language
@babel.localeselector
def get_locale():
	if 'username' in session:
		return 'de'
	return 'fr'

if __name__ == '__main__':
	# set the debug mode.
	app.debug = True

	# set the secret key.  keep this really secret:
	app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

	# set the default locale language
	app.config['BABEL_DEFAULT_LOCALE'] = 'en'

	app.run(host='0.0.0.0')