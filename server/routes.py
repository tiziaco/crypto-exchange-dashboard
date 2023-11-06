from pathlib import Path
import re

from flask import current_app as app
from flask import render_template


@app.route("/")
def index():
	return "<h1> Server connected </h1>"