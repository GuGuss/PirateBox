@app.route('/hello')
def helloworld_hello():
	return render_layout(extension_render_template('helloworld/hello.html'))