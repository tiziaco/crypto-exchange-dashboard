from flask import render_template, jsonify
from flask import Blueprint

views_blueprint = Blueprint('views', __name__)

@views_blueprint.route("/")
def index():
	return render_template(
			"index.html",
			# content=Markup(html),
			# styles=Markup(styles),
		)

@views_blueprint.route('/api/test', methods=['GET'])
def test_api():
    # Replace this with your actual data retrieval logic
    data = {'key': 'value', 'foo': 'bar'}

    return jsonify(data)