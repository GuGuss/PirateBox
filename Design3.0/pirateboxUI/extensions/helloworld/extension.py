@app.route('/hello')
def helloworld_hello():
	return render_layout(render_extension_template('helloworld/hello.html'))