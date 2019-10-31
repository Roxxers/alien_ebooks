from flask import render_template

from alien_ebooks import app


@app.route("/")
def index():
    return render_template("index.html", info=app.config["INFO"])
