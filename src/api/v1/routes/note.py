from bson.objectid import ObjectId
from flask import Blueprint,request,jsonify
from pymongo import MongoClient
from src.config.config import MONGODB_URI

note = Blueprint('note',__name__,url_prefix="/api/note")

mongo = MongoClient(MONGODB_URI)
db = mongo.remongo_db
notes = db.notes

class SerializeData:

    def __init__(self,needed_attributes):
        self.needed_attributes = needed_attributes

    def serialize(self, data):
        result = {}
        for attr in self.needed_attributes:
            if attr == '_id':
                result[attr] = str(data[attr])
            else:
                result[attr] = data[attr]
        return result

    def dump(self,data_list):
        result = []
        for index in range(len(data_list)):
            data = self.serialize(data_list[index])
            result.append(data)
        return result
        

@note.get("/")
def add_note():
    db_response = notes.insert_one({'name':"First",'body':"Just a body"})
    print(db_response)
    return jsonify({'error':False,'message':"Note Created"}),200

@note.get("/one")
def get_one():
    db_res = notes.find({'name':"First"})
    result = SerializeData(['_id','name','body']).dump(list(db_res))
    print(list(db_res))
    return jsonify({'data':result})