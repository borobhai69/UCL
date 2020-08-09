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
app.secret_key = '_5#z2L"F4Q8z\n\xec]/'
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
        return render_template('predict.html', time=datetime.now(), session = session)
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
        session["username"] = name
        session_name = session["username"]
        session["atalanta"] = atalanta
        session_atalanta = session["atalanta"]
        session["psg"] = psg
        session_psg = session["psg"]
        session["atletico"] = atletico
        session_atletico = session["atletico"]
        session["leipzig"] = leipzig
        session_leipzig = session["leipzig"]
        session["bayern"] = bayern
        session_bayern = session["bayern"]
        session["barcelona"] = barcelona
        session_barcelona = session["barcelona"]
        session["mancity"] = mancity
        session_mancity = session["mancity"]
        session["lyon"] = lyon
        session_lyon = session["lyon"]
        # insert new data
        predictions.insert({'name': session_name, 'atalanta': session_atalanta, 'psg': session_psg, 'atletico': session_atletico, 'leipzig': session_leipzig, 'bayern': session_bayern, 'barcelona': session_barcelona, 'mancity': session_mancity, 'lyon': session_lyon})
        predictions = mongo.db.predictions
        predictview = list(predictions.find({}))
        # print(predictview)
        # return a message to the user
        return redirect('/')
        return render_template('index.html', time=datetime.now(), predictview = predictview, name = session_name, atalanta = session_atalanta, psg = session_psg, atletico = session_atletico, leipzig = session_leipzig, bayern = session_bayern, barcelona = session_barcelona, mancity = session_mancity, lyon = session_lyon)
