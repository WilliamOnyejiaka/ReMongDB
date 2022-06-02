from . import db 
from datetime import datetime
from src.modules.Serializer import Serializer
from bson.objectid import ObjectId

notes = db.notes

class Note:

    @staticmethod
    def add_note(title:str,body:str,user_id:str) -> bool:
        db_response = notes.insert_one({
            'title':title,
            'body':body,
            'user_id':user_id,
            'created_at':datetime.now(),
            'updated_at':None
        })

        return True if db_response else False
    
    @staticmethod
    def get_note(id: str, user_id: str, needed_attributes: str = ['_id', 'title', 'body', 'user_id', 'created_at', 'updated_at']):
        query = notes.find_one({'_id': ObjectId(id), 'user_id': user_id})
        return Serializer(needed_attributes).serialize(query) if query else {}
