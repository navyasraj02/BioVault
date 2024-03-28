from flask import Flask
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask_cors import CORS
import os
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY')
app.config["MONGO_URI"] = "mongodb+srv://donajohn31:Progband@cluster1.u0j3wol.mongodb.net/biovault?retryWrites=true&w=majority"
# app.config["MONGO_URI"] = os.environ.get('MONGO_URI') ---NOT WOKRING 
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg','tif'}
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'sample')

# mongodb database
mongodb_client = PyMongo(app)
db = mongodb_client.db
CORS(app)

CORS(app, "origins": "*")
from application import routes