from flask import Flask, url_for
from mongodb import *
import json
from bson.objectid import ObjectId
from flask import jsonify
from flask import render_template
import datetime

date=datetime.datetime.now()
dt_string_date = date.strftime("%d-%m-%Y")

collection=mydatabase.binance_currency
collection_fear=mydatabase.fear_index

app = Flask(__name__)

@app.route("/")
def get_info():
    fear_info=[]
    for f_info in collection_fear.find().sort('timestamp', -1):
        f_info['_id']=str(f_info['_id'])
        f_info['timestamp'] =(datetime.datetime.fromtimestamp(int(f_info['timestamp']))).strftime("%d-%m-%Y")
        fear_info.append(f_info)
    return render_template('main.html', fear_info=fear_info[:1])

@app.route("/<time>")
def get_timeframe_info(time):
    info=[]
    for inf  in collection.find({'time frame':f'{str(time)}'}).sort([("date", -1),("time", -1)]):
        inf['_id']=str(inf['_id'])
        inf['time']=str(inf['time'])
        info.append(inf)
    return render_template('index.html', info=info[:12])
# with app.test_request_context():
#     print(url_for('get_in', time='1h'))
if __name__=='__main__':
    app.run(debug=True)