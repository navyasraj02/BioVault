from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["SECRET_KEY"] = "db24c608640f5034b30b8e1e1eb5618ed0ffdbf5"
app.config["MONGO_URI"] = "mongodb+srv://donajohn31:Progband@cluster1.u0j3wol.mongodb.net/biovault?retryWrites=true&w=majority"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = 'sample'

# mongodb database
mongodb_client = PyMongo(app)
db = mongodb_client.db

from application import routes