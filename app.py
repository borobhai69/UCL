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
        for item in predictview:
            print(item)
        # return a message to the user
        return redirect('/')
        return render_template('index.html', time=datetime.now(), predictview = predictview, name = session_name, atalanta = session_atalanta, psg = session_psg, atletico = session_atletico, leipzig = session_leipzig, bayern = session_bayern, barcelona = session_barcelona, mancity = session_mancity, lyon = session_lyon)

@app.route('/match_one')
def match_one():
    final_atalanta = 1
    final_psg = 2
    predictions = mongo.db.predictions
    predictview = list(predictions.find({}))
    matchone_ten = []
    matchone_four = []
    matchone_zero = []
    for score in predictview:
        if int(score["atalanta"]) == final_atalanta and int(score["psg"]) == final_psg:
            matchone_ten.append(score["name"])
        elif int(score["atalanta"]) < int(score["psg"]):
            matchone_four.append(score["name"])
        elif int(score["atalanta"]) > int(score["psg"]):
            matchone_zero.append(score["name"])
        else:
            matchone_zero.append(score["name"])
    for name in matchone_ten:
        predictions.update({'name': name}, {"$set": {'points1': 10}})
    for name in matchone_four:
        predictions.update({'name': name}, {"$set": {'points1': 4}})
    for name in matchone_zero:
        predictions.update({'name': name}, {"$set": {'points1': 0}})
    return render_template('index.html', time=datetime.now())

@app.route('/match_two')
def match_two():
    final_atletico = 1
    final_leipzig = 2
    predictions = mongo.db.predictions
    predictview = list(predictions.find({}))
    matchtwo_ten = []
    matchtwo_four = []
    matchtwo_zero = []
    for score in predictview:
        if int(score["atletico"]) == final_atletico and int(score["leipzig"]) == final_leipzig:
            matchtwo_ten.append(score["name"])
        elif int(score["atletico"]) < int(score["leipzig"]):
            matchtwo_four.append(score["name"])
        elif int(score["atletico"]) > int(score["leipzig"]):
            matchtwo_zero.append(score["name"])
        else:
            matchtwo_zero.append(score["name"])
    for name in matchtwo_ten:
        predictions.update({'name': name}, {"$set": {'points2': 10}})
    for name in matchtwo_four:
        predictions.update({'name': name}, {"$set": {'points2': 4}})
    for name in matchtwo_zero:
        predictions.update({'name': name}, {"$set": {'points2': 0}})
    return render_template('index.html', time=datetime.now())

@app.route('/total')
def total():
    predictions = mongo.db.predictions
    predictview = list(predictions.find({}))
    for item in predictview:
        point1 = item["points1"]
        point2 = item["points2"]
        total = point1 + point2
        predictions.update({'name': item["name"]}, {"$set": {'total': total}})
    return render_template('index.html', time=datetime.now())