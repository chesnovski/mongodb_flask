from pymongo import MongoClient
import json
import pprint
client = MongoClient('localhost', 27017)
mydatabase = client.currency
collections = mydatabase.list_collection_names()
# print(collections)

# def inser_text_doc():
#     collection=mydatabase.nn
#     test_doc={
#         'name':'aaa',
#         'type':'pies'    }
#     inserted_id=collection.insert_one(test_doc).inserted_id
#     print(inserted_id)
# inser_text_doc()

# collection = db.nn
# print(collection)
printer=pprint.PrettyPrinter()
collection=mydatabase.time_frame_1h
# def find_all():
#     coin=collection.find({'data': '14-12-2022 11:49','symbol': 'ETHUSDT' })
#     for i in coin:
#         i
#     return i
# print(find_all)

