@app.route('/map')
def openstreetmap_map():
	return render_layout(extension_render_template('openstreetmap/OSM_In_A_Box_beta.html'))