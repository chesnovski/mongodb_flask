import pyrebase
import json
config={
    'apiKey': "AIzaSyBZOSz3HBKY4A2k3I2fGnMlsBr3j9wQcsM",
    'authDomain': "currencydata-f3265.firebaseapp.com",
    'projectId': "currencydata-f3265",
    'databaseURL': "https://currencydata-f3265-default-rtdb.firebaseio.com/",
    'storageBucket':"currencydata-f3265.appspot.com",
    'messagingSenderId': "265616502124",
    'appId': "1:265616502124:web:70453610b1c16cc8f79749",
    'measurementId': "G-2BSW3BJSL0"
 }

firebase=pyrebase.initialize_app(config)
database=firebase.database()
  
