from application import app
from flask import render_template, request, redirect, flash, url_for
import os
from PIL import Image
from werkzeug.utils import secure_filename
from bson import ObjectId

from .route_func import pinGen
from .forms import UserData
from application import db

@app.route("/")
def index():
    return "<p> Hello World!</p>"


@app.route("/get_user_data", methods=["POST","GET"])
def get_user_data():
    if request.method== "POST":
        form = UserData()
        if form.validate_on_submit():
            user_fimg = request.files.get('fimg')
            if user_fimg:
                user_name = form.name.data
                user_email = form.email.data
            
                filename = secure_filename(user_fimg.filename)
                userFile = os.path.join("sample", filename)
                upload_folder = app.config['UPLOAD_FOLDER']
                s = user_fimg.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), upload_folder, filename))
                print("File saved successfully:", userFile)

                db.regUser.insert_one({
                    "name" : user_name,
                    "email" : user_email
                    
                })

                print("Sign Up Successful","success")
                pinGen.generate_secure_token()
                return redirect("/")
            else:
                flash("No file uploaded", "error")
    else:
        form = UserData()
    return render_template("get_user_data.html",form = form)