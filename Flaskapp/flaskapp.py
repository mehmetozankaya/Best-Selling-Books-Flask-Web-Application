# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 04:42:32 2021

@author: ozank
"""
from flask import Flask, render_template
import pymongo
from bson.json_util import dumps
#from flask_table import Table, Col
import pandas as pd


app = Flask(__name__)


#connecting to mongodb
try:
 client = pymongo.MongoClient("mongodb+srv://ozan:kaya@cluster0.2v7o6.mongodb.net/<dbname>?retryWrites=true&w=majority")
 print("Connected to cruise MongoClient Successfully from Project Script!!!")
except:
 print("Connection to MongoClient Failed!!!")

db=client["AmazonData"]
col = db["BestBooks"]
cur2=db["BestBooks"].find(return_key=False)
df =  pd.DataFrame(list(cur2))
del df['_id'] #deleting id column from mongoDB
df.index += 1 #fixing index
print(df)


#home page
@app.route("/")

def home():
  return render_template("home.html")

#showing raw data in /data
@app.route("/data")
def results():
    try:
        htmldata= df.to_html()
        return htmldata
    except Exception as e:
        return dumps({'error': str(e)})

@app.route("/tables")
def show_tables():
    data = df
    return render_template('view.html',tables=[data.to_html()],

    titles = ['na', 'Best Books'])



@app.route("/about")
def about():
  return render_template("about.html")


if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)