from application import app
from flask import jsonify, render_template, request, redirect, flash, url_for
import os
from PIL import Image
from werkzeug.utils import secure_filename
from bson import ObjectId

from .route_func import pinGen,fpMatch  
from .forms import UserData
from application import db

folder_name = "sample"

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
            
                # filename = secure_filename(user_fimg.filename)
                # userFile = os.path.join("sample", filename)
                # upload_folder = app.config['UPLOAD_FOLDER']
                # s = user_fimg.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), upload_folder, filename))
                # print("File saved successfully:", userFile)

                print("Sign Up Successful","success")
                pinGen.generate_secure_token()
                # Get the absolute path to the folder where your script is located
                script_dir = os.path.abspath(os.path.dirname(__file__))

                # Construct the path to the file using os.path.join
                file_path1 = os.path.join(script_dir, folder_name, "fa1.BMP")
                file_path2 = os.path.join(script_dir, folder_name, "fa2.BMP")

                # # Check if the file exists before attempting to open it
                # if os.path.exists(file_path):
                #     # Now you can do whatever you want with the file, such as opening it
                #     with open(file_path, "r") as file:
                        
                score=fpMatch.fingerprint_similarity(file_path1,file_path2)
                print("Matching score: ",score)
                """db.regUser.insert_one({
                    "name" : user_name,
                    "email" : user_email
                    
                }) """

                
                return redirect("/")
            else:
                flash("No file uploaded", "error")
    else:
        form = UserData()
    return render_template("get_user_data.html",form = form)