# ---- YOUR APP STARTS HERE ----
# -- Import section --
from flask import Flask
from flask import render_template
from flask import request
from flask_pymongo import PyMongo, ObjectId
from flask import redirect
from flask import session, url_for
from datetime import datetime
import pprint
import os

# -- Initialization section --
app = Flask(__name__)

user = os.environ["user"]
pw = os.environ["pw"]

# name of database
app.config['MONGO_DBNAME'] = 'ucl-2020'

# URI of database
app.config['MONGO_URI'] = f'mongodb+srv://{user}:{pw}@cluster0.hmonv.mongodb.net/ucl-2020?retryWrites=true&w=majority'

mongo = PyMongo(app)

# -- Routes section --
# INDEX

@app.route('/')
@app.route('/index')

def index():
    predictions = mongo.db.predictions
    predictview = list(predictions.find({}))
    return render_template('index.html', time = datetime.now(), predictview = predictview)


# CONNECT TO DB, ADD DATA

@app.route('/getpredictions', methods = ["GET", "POST"])

def getpredictions():
    if request.method == "GET":
        return render_template('predict.html', time=datetime.now())
    else:
        # this is storing the data from the form 
        name = request.form['name']
        atalanta = request.form['atalanta']
        psg = request.form['psg']
        atletico = request.form['atm']
        leipzig = request.form['rbl']
        bayern = request.form['bayern']
        barcelona = request.form['barca']
        mancity = request.form['mancity']
        lyon = request.form['lyon']
        # this is connecting to mongodb
        predictions = mongo.db.predictions
        # insert new data
        predictions.insert({'name': name, 'atalanta': atalanta, 'psg': psg, 'atletico': atletico, 'leipzig': leipzig, 'bayern': bayern, 'barcelona': barcelona, 'mancity': mancity, 'lyon': lyon})
        predictions = mongo.db.predictions
        predictview = list(predictions.find({}))
        # print(predictview)
        # return a message to the user
        return render_template('index.html', time=datetime.now(), predictview = predictview, name = name, atalanta = atalanta, psg = psg, atletico = atletico, leipzig = leipzig, bayern = bayern, barcelona = barcelona, mancity = mancity, lyon = lyon)
