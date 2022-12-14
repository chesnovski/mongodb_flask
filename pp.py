from pymongo import MongoClient
import json
client = MongoClient('localhost', 27017)
mydatabase = client.data
collections = mydatabase.list_collection_names()
print(collections)

def inser_text_doc():
    collection=mydatabase.nn
    test_doc={
        'name':'aaa',
        'type':'pies'    }
    inserted_id=collection.insert_one(test_doc).inserted_id
    print(inserted_id)
inser_text_doc()

# collection = db.nn
# print(collection)