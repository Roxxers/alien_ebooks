from flask import session, redirect, request, url_for, jsonify, render_template, abort
from subredditgenerator import app


@app.route("/")
def index():
    return render_template("index.html")
