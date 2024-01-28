from flask import Flask
##from flask_pymongo import PyMongo

app = Flask(__name__)
##app.config["MONGO_URI"] = "mongodb+srv://donajohn31:Prgo1@band@cluster.kebfxpl.mongodb.net/?retryWrites=true&w=majority"
##mongo = PyMongo(app)

@app.route("/")
def hello_world():
    return "<p> Hello World</p>"

app.run(debug=True)