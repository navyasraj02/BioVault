from application import app
from flask import jsonify, render_template, request, redirect, flash, url_for
import os
import requests
import numpy as np
from PIL import Image
from werkzeug.utils import secure_filename
import msgpack
from .route_func import pinGen,fpMatch
from .route_func.encryption import segEnc2, random_gen,transform
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
    name = request.form.get("name")
    email = request.form.get("email")
    #phoneno = request.form.get("phoneno")
    #print("phone no:",phoneno)
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
            "email" : email,
            #"phoneno" : phoneno            
        }).inserted_id
        print("Id: ",user_id)

        # Encrypt user_id by applying transformations - RC4 and SHA256
        t_id = transform.hash_string(str(user_id))
        print("Transformed Id: ",t_id)

        # Generate random server nos 
        random_snos = random_gen.generate_random_numbers(t_id)
        s=[]
        print('Random server nos: ',random_snos)
        '''for i in range(4):
            server=fpMatch.server(random_snos[i])
            response = requests.post(
            server[i]+"/api/log", json={"data":data},headers={"Content-Type": "application/json"})
            print("sent: from main server") 
            if response.status_code!=200:
                return jsonify({"error":"error sending to storage server"+i})
            response_data = json.loads(response.content)'''

            
        

        # Segment fingerprint into 4 parts change the image to image recieved from the front end
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
        keypoint_1 = kp_s[0]
        descrip_1 = desc[0]
        user_id_1= t_id
        
        data = {
            "len":len(keypoint_1),
            #"keypoint": skeypoint_1.tolist(),
            "descrip": descrip_1.tolist(),
            "user_id": user_id_1,
        }
        #data=msgpack.dumps(data)
        # Send POST request to receiving server
        response = requests.post(
            "https://biovault-server1.onrender.com/api/reg", json={"data":data},headers={"Content-Type": "application/json"})
        print("sent: from main server") 
        if response.status_code!=200:
            return jsonify({"error":"error sending to storage server"})   
        print(response.content)  

        

        # delete_files(sample_dir)
        return {"message" :"Registration successful","success": True}

@app.route("/api/login", methods=["POST","GET"])
def login():
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

        # Retrieve object_id of user
        user_id = existing_user['_id']
        print("Id: ", user_id)

        print("applying transformation")
        # Encrypt user_id by applying transformations - RC4 and SHA256
        t_id = transform.hash_string(str(user_id))
        print("Transformed Id: ",t_id)

        # Generate random server nos 
        random_snos = random_gen.generate_random_numbers(t_id)
        print('Random server nos: ',random_snos)

        # Segment fingerprint into 4 parts
        #kp_s,desc= fpMatch.fingerprint_segment(os.path.join(sample_dir,"fa1.BMP"))
        # print("kp_s: ",kp_s)
        # print("desc: ",desc)

        # Retrieve the server public keys 
        pub_keys = segEnc2.get_public_keys(random_snos)
        '''for i in range(4):
            server=fpMatch.server(random_snos[i])
            response = requests.post(
            server[i]+"/api/log", json={"data":data},headers={"Content-Type": "application/json"})
            print("sent: from main server") 
            if response.status_code!=200:
                return jsonify({"error":"error sending to storage server"+i})
            response_data = json.loads(response.content)

            # Check if the response indicates success and get the score if present
            if response_data.get("success") == "true":
                score = response_data.get("score")
                s.append(score)
                print("Score:", score)
            else:
                print("Response indicates failure")   
                print(response.content)'''
        

        
        return {"message" :"Login successful","success": True}
    else:
        print("User not found: ",existing_user)
        return jsonify({"success":False}), 409
        

"""@app.route("/api/login", methods=["POST","GET"])
def login():
    name=request.form.get("name")
    email=request.form.get("email")
    fpimg=request.files['fingerprint']
    existing_user = db.regUser.find_one({"email": email})
    if existing_user:
        print("User found: ",existing_user)
        filename = secure_filename(fpimg.filename)
        fpimg.save(os.path.join(sample_dir, filename))
        print("File saved successfully")
        kp_s,desc= fpMatch.fingerprint_segment(os.path.join(sample_dir,"fa1.BMP"))
        randomno=random_gen.generate_random_numbers(existing_user._id)
        print(randomno)
        return jsonify({"exists": True,"success":False}), 409
    else:
        return {"message":"No such User exists!!!"}"""  

# --------delete file func---------
def delete_files(folder_path):
    # folder_path = 'path/to/your/folder'

    file_list = os.listdir(folder_path)

    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)
        os.remove(file_path)