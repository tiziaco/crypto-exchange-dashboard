from pathlib import Path
from flask import render_template
import re

from flask import current_app as app


@app.route("/")
def index():
	return render_template(
			"index.html",
			# content=Markup(html),
			# styles=Markup(styles),
		)