from pymongo import MongoClient
import json
import pprint
from pymongo.errors import ServerSelectionTimeoutError
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

mongodb_token = (os.getenv('mongo_db_client'))


def connection_with_db():
    maxSevSelDelay = 1
    # client = MongoClient('localhost', 27017,serverSelectionTimeoutMS=maxSevSelDelay)
    client = MongoClient(mongodb_token)
    mydatabase = client.currency
    # try:
    #     info = client.server_info() # Forces a call.

    return mydatabase
    # except ServerSelectionTimeoutError:
    #     return print("server is down.")







