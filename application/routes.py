from application import app
from flask import jsonify, render_template, request, redirect, flash, url_for
import os
from PIL import Image
from werkzeug.utils import secure_filename

from .route_func import pinGen,fpMatch
from .route_func.encryption import segEnc2, random_gen
from .forms import UserData
from application import db

APP_ROOT = os.path.abspath(os.path.dirname(__file__))
parent_dir = os.path.dirname(APP_ROOT)
sample_dir = os.path.join(parent_dir, 'sample')

@app.route("/")
def index():
    return  {"status": "success", "message": "Integrate Flask Framework with Next.js"}

@app.route("/api/login", methods=["POST","GET"])
def login():
    name=request.form.get("name")
    email=request.form.get("email")
    fpimg=request.files['fingerprint']
    existing_user = db.regUser.find_one({"email": email})
    if existing_user:
        print("User found: ",existing_user)
        #return jsonify({"exists": True,"success":False}), 409
        filename = secure_filename(fpimg.filename)
        fpimg.save(os.path.join(sample_dir, filename))
        print("File saved successfully")
        kp_s,desc= fpMatch.fingerprint_segment(os.path.join(sample_dir,"fa1.BMP"))
        randomno=random_gen.generate_random_numbers(existing_user._id)
        print(randomno)
        return jsonify({"exists": True,"success":False}), 409
    else:
        return {"message":"No such User exists!!!"}

        

@app.route("/api/register", methods=["POST","GET"])
def register():
    name = request.form.get("name")
    email = request.form.get("email")
    fpimg = request.files['fingerprint']

    filename = secure_filename(fpimg.filename)
    fpimg.save(os.path.join(sample_dir, filename))
    print("File saved successfully")

    # Check for existing email id
    existing_user = db.regUser.find_one({"email": email})
    if existing_user:
        print("User found: ",existing_user)
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

        # Retrieve the server public keys 
        pub_keys = segEnc2.get_public_keys(random_snos)
        # for i in random_snos:
        #     print("Server ",i," : ",pub_keys[i])

        # Encrypt the segments 
        # for i in range(4):
        #     # print(random_snos[i],": ",pub_keys[random_snos[i]])
        #     encrpted_seg = segEnc2.encrypt_segment(pub_keys[random_snos[i]],kp_s[i])
        #     print("Encrypted segment ",i+1,": ",encrpted_seg)
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