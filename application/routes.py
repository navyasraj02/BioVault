from application import app
from flask import jsonify, render_template, request, redirect, flash, url_for
import os
from PIL import Image
from werkzeug.utils import secure_filename

from .route_func import pinGen,fpMatch
from .route_func.encryption import random_gen 
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
    # print("File saved successfully")

    # Check for existing email id
    existing_user = db.users.find_one({"email": email})
    if existing_user:
        print("user found: ",existing_user)
        return jsonify({"exists": True,"success":False}), 409
    else:

        # Retrieve object_id of user
        user_id = db.regUser.insert_one({
            "name" : name,
            "email" : email             
        }).inserted_id
        print("Id: ",user_id)

        # Generate random server nos from user_id
        random_snos = random_gen.generate_random_numbers(user_id)
        print('Random server nos: ',random_snos)

        # Segment fingerprint into 4 parts
        kp_s,desc= fpMatch.fingerprint_segment(os.path.join(sample_dir,"fa1.BMP"))
        # print("kp_s: ",kp_s)
        # print("desc: ",desc)

        # Send segments to random servers

       
        '''"segments": [
        {
            "segment_id": 1,
            "keypoints": kp_s1[0]  // Convert to a Python list for storage
        }'''

        # delete_files(sample_dir)
        return {"message" :"Registration successful","success": True}

# --------delete file func---------
def delete_files(folder_path):
    # folder_path = 'path/to/your/folder'

    file_list = os.listdir(folder_path)

    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)
        os.remove(file_path)