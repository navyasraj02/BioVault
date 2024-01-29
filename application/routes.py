from application import app
from flask import render_template, request, redirect, flash, url_for

from bson import ObjectId

from .forms import UserData
from application import db

@app.route("/")
def index():
    return "<p> Hello World!</p>"


@app.route("/get_user_data", methods=["POST","GET"])
def get_user_data():
    if request.method== "POST":
        form = UserData(request.form)
        user_name = form.name.data
        user_email = form.email.data

        db.regUser.insert_one({
            "name" : user_name,
            "email" : user_email
        })

        flash("Sign Up Successful","success")
        return redirect("/")
    else:
        form = UserData()
    return render_template("get_user_data.html",form = form)