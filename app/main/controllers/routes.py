from pathlib import Path
from flask import render_template, jsonify

from flask import current_app as app


@app.route("/")
def index():
	return render_template(
			"index.html",
			# content=Markup(html),
			# styles=Markup(styles),
		)

@app.route('/api/test', methods=['GET'])
def test_api():
    # Replace this with your actual data retrieval logic
    data = {'key': 'value', 'foo': 'bar'}
    
    # Return the data as JSON
    return jsonify(data)