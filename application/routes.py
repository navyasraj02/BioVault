from application import app
from flask import render_template, request, redirect, flash, url_for

from bson import ObjectId

from .forms import userData
from application import db
from datetime import datatime

@app.route("/")
def get_user_data():
    user_data = []
    for data in db.