from flask import Flask, url_for, session, redirect, render_template, request
from mongodb import connection_with_db
import json
from bson.objectid import ObjectId
from flask import jsonify
import datetime
from market_movers import*
import secrets
from flask_wtf import FlaskForm
from wtforms.fields import DateField, SelectField
from wtforms.validators import DataRequired
from wtforms import validators, SubmitField

now_date = datetime.datetime.now()
dt_string_date = now_date.strftime("%d-%m-%Y")
mydatabase = connection_with_db()
collection = mydatabase.binance_currency
collection_fear = mydatabase.fear_index
collection_stocks_currency = mydatabase.stocks_currency



app = Flask(__name__)
secret = secrets.token_urlsafe(32)

app.secret_key = secret

class InfoFrom(FlaskForm):
    date = DateField('Start Date', format='%Y-%m-%d', validators=(validators.DataRequired(),))
    time_frame = SelectField ('Time Frame', choices=[('15m', '15m '), ('1h', '1h'), ('4h', '4h'), ('1d', '1d')] )
    submit = SubmitField('Submit')


@app.route("/")
def main():
    list_news 
    return render_template('main.html', list_news=list_news)



@app.route("/feargreed")
def get_info():
    fear_info=[]
    for f_info in collection_fear.find().sort('timestamp', -1):
        f_info['_id']=str(f_info['_id'])
        f_info['timestamp'] =(datetime.datetime.fromtimestamp(int(f_info['timestamp']))).strftime("%d-%m-%Y")
        fear_info.append(f_info)
    return render_template('feargreed.html', fear_info=fear_info[:1])

@app.route("/currency", methods=['GET', 'POST'])
def get_timeframe_info():
    form = InfoFrom()
    print(form.time_frame.data)
    if form.validate_on_submit():
        # session['date'] = form.date.data
        input_date = form.date.data
        new_format_date = input_date.strftime("%d-%m-%Y")
        time = form.time_frame.data
    else: 
        new_format_date = dt_string_date 
        time = '15m'
    info=[]
    for inf  in collection.find({'time frame':f'{str(time)}', 'date':f'{str(new_format_date)}'}).sort('timestamp', -1):
        inf['_id']=str(inf['_id'])
        inf['time']=str(inf['time'])
        info.append(inf)
    return render_template('index.html', info=info[:12] ,form=form, time=time)




@app.route("/stocks", methods=['GET','POST'])
def get_stocks_info():
    form = InfoFrom()
    if form.validate_on_submit():
        # session['date'] = form.date.data
        input_date = form.date.data
        new_format_date = input_date.strftime("%d-%m-%Y")
        time = form.time_frame.data
    else: 
        new_format_date = dt_string_date
        time = '15m'
    stock_info=[]
    for inf  in collection_stocks_currency.find({'time frame':f'{str(time)}', 'date':f'{str(new_format_date)}'}).sort('timestamp', -1):
        inf['_id']=str(inf['_id'])
        inf['time']=str(inf['time'])
        # inf['change price']=float(inf['change price'])
        stock_info.append(inf)
    session['stock'] = stock_info
    return render_template('stocks.html', stock_info=stock_info[:12], form=form, time=time)





@app.route("/info/<symbol>&<exchange>")
def get_coin_info(symbol, exchange):
    d = f'{exchange}:{symbol}'
    return render_template('test.html', d = d)
if __name__=='__main__':
   app.run(host='0.0.0.0', port=5000)
