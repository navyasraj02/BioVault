from application import app
from flask import abort,jsonify, render_template, request, redirect, flash, url_for
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
    #fpimg = request.files['image']

    #filename = secure_filename(fpimg.filename)
    #fpimg.save(os.path.join(sample_dir, filename))
    print("File saved successfully")

    #Perform encryption logic  
    
    user = db.users.find_one({"email": email})
    print("user:",user)
    if user:                                                                                                                                                                                                                     
        return jsonify({"exists": True,"success":False,"message": "User with email already exists" }), 409
    else:
        

# --------delete file func---------
def delete_files(folder_path):
    # folder_path = 'path/to/your/folder'

    file_list = os.listdir(folder_path)

    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)
        os.remove(file_path)