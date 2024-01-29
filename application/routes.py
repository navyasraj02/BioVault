from application import app
from flask import render_template, request, redirect, flash, url_for

from bson import ObjectId

from .forms import UserData
# from application import db
# from datetime import datatime

@app.route("/")
def index():
    return "<p> Hello World!</p>"


@app.route("/get_user_data")
def get_user_data():
    form = UserData()
    return render_template("get_user_data.html",form = form)