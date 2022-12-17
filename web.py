from flask import Flask
from mongodb import *
import json
from bson.objectid import ObjectId
from flask import jsonify
from flask import render_template
import datetime

date=datetime.datetime.now()
dt_string_date = date.strftime("%d-%m-%Y")

collection1h=mydatabase.time_frame_1h
collection15m=mydatabase.time_frame_15m
collection4h=mydatabase.time_frame_4h
collection1d=mydatabase.time_frame_1d

app = Flask(__name__)

menu=['15 minutes', '1 hour', '4 hours', '1 day']

@app.route("/")
def get_info():
    return render_template('main.html')


@app.route("/1h")
def get_1h():
    info=[]
    for inf  in collection1h.find({'date':f'{dt_string_date}'}).sort("time", -1):
        inf['_id']=str(inf['_id'])
        inf['time']=str(inf['time'])
        info.append(inf)
    return render_template('index.html', info=info[:12])

@app.route("/15m")
def get_15m():
    info=[]
    for inf  in collection15m.find({'date':f'{dt_string_date}'}).sort("time", -1):
        inf['_id']=str(inf['_id'])
        inf['time']=str(inf['time'])
        info.append(inf)
    return render_template('index.html', info=info[:12])

@app.route("/4h")
def get_4h():
    info=[]
    for inf  in collection4h.find({'date':f'{dt_string_date}'}).sort("time", -1):
        inf['_id']=str(inf['_id'])
        inf['time']=str(inf['time'])
        info.append(inf)
    return render_template('index.html', info=info[:12])

@app.route("/1d")
def get_1d():
    info=[]
    for inf  in collection1d.find({'date':f'{dt_string_date}'}).sort("time", -1):
        inf['_id']=str(inf['_id'])
        inf['time']=str(inf['time'])
        info.append(inf)
    return render_template('index.html', info=info[:12])



@app.route('/services')
def services():
    return render_template('test.html')

if __name__=='__main__':
    app.run(debug=True)