from application import app
from flask import jsonify, render_template, request, redirect, flash, url_for
import os
import requests
import numpy as np
from PIL import Image
from werkzeug.utils import secure_filename
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
        print('Random server nos: ',random_snos)
        
        # Fingerprint segmentation
        kp_s,desc= fpMatch.fingerprint_segment(os.path.join(sample_dir,"fa1.BMP"))
        
        user_id_1= t_id
        #print(desc[0].tolist())

        # Send segments to random servers
        s=[]        
        for i in range(4):
            server=fpMatch.server(random_snos[i])
            data = {
            "len":len(kp_s[i]),
            #"keypoint": skeypoint_1.tolist(),
            "descrip": desc[i].tolist(),
            "user_id": user_id_1}
            response = requests.post(
            server+"/api/reg", json={"data":data},headers={"Content-Type": "application/json"})
            print("Sent: from main server to storage server ",server) 
            if response.status_code!=201:
                print("Error from storageserver")
                print(response)
                result = db.regUser.delete_one({'_id': user_id})
                # Check if the deletion was successful
                if result.deleted_count == 1:
                    print("User deleted successfully.")
                else:
                    print("User not found.")
                return jsonify({"error":"error sending to storage server"})
            

        # Retrieve the server public keys 
        #pub_keys = segEnc2.get_public_keys(random_snos)

        # Encrypt the segments 
        # for i in range(4):
        #     # print(random_snos[i],": ",pub_keys[random_snos[i]])
        #     encrpted_seg = segEnc2.encrypt_segment(pub_keys[random_snos[i]],kp_s[i])
        #     print("Encrypted segment ",i+1,": ",encrpted_seg)

        #delete files
        delete_files(sample_dir)
        print(sample_dir)
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

        print("Applying transformation")
        # Encrypt user_id by applying transformations - RC4 and SHA256
        t_id = transform.hash_string(str(user_id))
        print("Transformed Id: ",t_id)

        # Generate random server nos 
        random_snos = random_gen.generate_random_numbers(t_id)
        print('Random server nos: ',random_snos)

        #Fingerprint segmentation
        kp_s,desc= fpMatch.fingerprint_segment(os.path.join(sample_dir,"fa1.BMP"))
        s=[]
        user_id_1= t_id

        # Retrieve the server public keys 
        #pub_keys = segEnc2.get_public_keys(random_snos)

        for i in range(4):
            server=fpMatch.server(random_snos[i])
            data = {
            "len":len(kp_s[i]),
            #"keypoint": skeypoint_1.tolist(),
            "descrip": desc[i].tolist(),
            "user_id": user_id_1}
            response = requests.post(
            server+"/api/log", json={"data":data},headers={"Content-Type": "application/json"})
            print("Sent: from main server to storage server ",server) 
            if response.status_code!=201:
                print("Error from server ",server)
                print(i)
                print(response)
                return jsonify({"error":"error sending to storage server"})
            

            # Check if the response indicates success and get the score if present
            if response.get("success") == "true":
                score = response.get("score")
                s.append(score)
                print("Score:", score)
            else:
                print("Response indicates failure")   
                print(response.content)
        print("outside for loop")
        s=np.array(s)
        all_above_50 = np.all(s> 50)
        #if all score is above 50 success and token send to front end acess
        if all_above_50:
            return jsonify({"message" :"Login successful","success": True})
        else:
           return jsonify({"message" :"Login failed","success": False})
                
    else:
        print("User not found: ",existing_user)
        return jsonify({"success":False}), 409
        

 

# --------delete file func---------
def delete_files(folder_path):
    # folder_path = 'path/to/your/folder'

    file_list = os.listdir(folder_path)

    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)
        os.remove(file_path)