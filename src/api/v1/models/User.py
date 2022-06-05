from typing import List
from . import db
from .Note import Note 
from werkzeug.security import generate_password_hash
from datetime import datetime
from bson.objectid import ObjectId
from src.modules.Serializer import Serializer

users = db.users

class User:

    @staticmethod
    def create_user(name:str,email:str,password:str):
        db_response = users.insert_one({
            'name':name,
            'email':email,
            'password':generate_password_hash(password),
            'created_at':datetime.now(),
            'updated_at':None
        })

        return True if db_response.inserted_id else False

    @staticmethod
    def get_user_with_email(email:str,needed_attributes:List=['_id','name','email','password','created_at','updated_at']):
        query = users.find_one({'email':email})
        if query:
            return Serializer(needed_attributes).serialize(query)
        return {}

    @staticmethod
    def get_user_with_id(id:str,needed_attributes:List=['_id','name','email','password','created_at','updated_at']):
        query = users.find_one({'_id':ObjectId(id)})
        return Serializer(needed_attributes).serialize(query) if query else {}

    @staticmethod
    def delete(id:str):
        query = users.find_one_and_delete({'_id':ObjectId(id)})
        if query:
            user_notes = Note.get_notes(id)
            for index in range(len(user_notes)):
                deleted = Note.delete(user_notes[index]['_id'],id)
            return True
        return False
