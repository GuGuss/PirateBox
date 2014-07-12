from flask import Flask, session, redirect, url_for, escape, request, render_template, render_template_string, g, request
from flaskext.babel import Babel, gettext, ngettext
import os
import codecs

app = Flask(__name__)

# Work with Flask Babel which handles translations
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
babel = Babel(app)



# TIPS
#gettext(u'You are logged in')
#Logged in as %s' % escape(session['username'])

# --------- #
# FUNCTIONS #
# --------- #

# include an existing extension
def extension_include(extension_name):
	file_name = 'extensions/' + extension_name + '/extension.py'
	if os.path.exists(file_name):
		execfile(file_name)
		print gettext(u'[Success] %(extension)s has been correctly included', extension=extension_name)
	else:
		print gettext(u'[Error] %(extension)s couldn\'t be included. "extension.py" file is missing.', extension=extension_name)

# check all existing extensions
def extension_check():
	for dir in os.listdir('extensions'):
		if os.path.isdir('extensions/' + dir):
			extension_include(dir)
			
# render an extension template
def extension_render_template(template, **context):
	with codecs.open('extensions/' + template, 'r', encoding='utf-8') as content_file:
		content = content_file.read()
	return render_template_string(content, context=context)

def render_layout(content, title=None):
	return render_template('layout.html', content=content, title=title)

@babel.localeselector
def get_locale():
	# try to guess the language from the user accept header the browser transmits
	return request.accept_languages.best_match(['de', 'fr', 'en'])

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
	return render_layout(render_template('concept.html'), 'Concept')

@app.route('/setup')
def setup():
	if 'username' in session:
		return render_layout(render_template('setup.html'), 'Setup')
	return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST' and request.form['password'] == 'password':
		session['username'] = 'admin'
		return redirect(url_for('setup'))
	return render_layout(render_template('login.html'), 'Login')

@app.route('/logout')
def logout():
	# remove the username from the session if it's there
	session.pop('username', None)
	return redirect(url_for('index'))


# load the available extensions
extension_check()


if __name__ == '__main__':
	# set the debug mode.
	app.debug = True

	# set the secret key.  keep this really secret:
	app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

	app.run(host='0.0.0.0')