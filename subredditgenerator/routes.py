from flask import session, redirect, request, url_for, jsonify, render_template, abort
from subredditgenerator import app


@app.route("/")
def index():
    return """<h1>hallo world</h1>"""
