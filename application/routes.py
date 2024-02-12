from application import app
from flask import jsonify, render_template, request, redirect, flash, url_for
import os
from PIL import Image
from werkzeug.utils import secure_filename

from .route_func import pinGen,fpMatch  
from .forms import UserData
from application import db

APP_ROOT = os.path.abspath(os.path.dirname(__file__))
parent_dir = os.path.dirname(APP_ROOT)
sample_dir = os.path.join(parent_dir, 'sample')

@app.route("/")
def index():
    return  {"status": "success", "message": "Integrate Flask Framework with Next.js"}

@app.route("/api/register", methods=["POST","GET"])
def register():
    name = request.json.get("name")
    email = request.json.get("email")
    fpimg = request.files['image']

    filename = secure_filename(fpimg.filename)
    fpimg.save(os.path.join(sample_dir, filename))
    print("File saved successfully")

    #Perform encryption logic  

    db.regUser.insert_one({
        "name" : name,
        "email" : email             
    })

    # delete_files(sample_dir)

    return jsonify({"message" : "Registration successfull"})

# --------delete file func---------
def delete_files(folder_path):
    # folder_path = 'path/to/your/folder'

    file_list = os.listdir(folder_path)

    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)
        os.remove(file_path)

    # if request.method== "POST":
    #     form = UserData()
    #     if form.validate_on_submit():
    #         user_fimg = request.files.get('fimg')
    #         if user_fimg:
    #             user_name = form.name.data
    #             user_email = form.email.data
            
    #             filename = secure_filename(user_fimg.filename)
    #             userFile = os.path.join("sample", filename)
    #             upload_folder = app.config['UPLOAD_FOLDER']
    #             # user_fimg.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), upload_folder, filename))
    #             # print("File saved successfully:", userFile)

    #             print("Sign Up Successful","success")
    #             # pinGen.generate_secure_token()
                
    #             #-----TO DO: file1 will be uploaded by user, file2 retrieved from the database-----
    #             # Construct the path to the file using os.path.join
    #             file_path1 = os.path.join(os.path.abspath(os.path.dirname(__file__)), upload_folder, "fa1.BMP")
    #             file_path2 = os.path.join(os.path.abspath(os.path.dirname(__file__)), upload_folder, "fa3.BMP")

    #             # Check if the file exists before attempting to open it
    #             if os.path.exists(file_path1) and os.path.exists(file_path2) :
    #                 score=fpMatch.fingerprint_similarity(file_path1,file_path2)
    #                 print("Matching score: ",score)

    #             """db.regUser.insert_one({
    #                 "name" : user_name,
    #                 "email" : user_email
                    
    #             }) """

    #             # Delete files from sample folder
    #             # delete_files(sample_dir)
    #             return redirect("/")
    #         else:
    #             flash("No file uploaded", "error")
    # else:
    #     form = UserData()
    # return render_template("get_user_data.html",form = form)
# MATCHING
#     file_path1 = os.path.join(sample_dir, "fa1.BMP")    # from user
#     file_path2 = os.path.join(sample_dir, "fa3.BMP")    # to be retrieved from DB
#     if os.path.exists(file_path1) and os.path.exists(file_path2) :
#         score=fpMatch.fingerprint_similarity(file_path1,file_path2)
#         print("Matching score: ",score)