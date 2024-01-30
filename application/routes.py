from application import app
from flask import render_template, request, redirect, flash, url_for
import os
from PIL import Image
from werkzeug.utils import secure_filename
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

        # print(form.errors)
        # print(form.validate_on_submit())

        if 'fimg' in request.files and form.validate_on_submit():
            print("hello")
            user_fimg = request.files['fimg']
            user_name = form.name.data
            user_email = form.email.data
        
            filename = secure_filename(user_fimg.filename)
            userFile = os.path.join("sample", filename)
            s = user_fimg.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'], filename))
            print("File saved successfully:", userFile)

            db.regUser.insert_one({
                "name" : user_name,
                "email" : user_email
                
            })

            flash("Sign Up Successful","success")
            return redirect("/")
    else:
        form = UserData()
    return render_template("get_user_data.html",form = form)