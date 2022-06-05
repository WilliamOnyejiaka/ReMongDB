from typing import Dict, List
from . import db
from datetime import datetime
from src.modules.Serializer import Serializer
from bson.objectid import ObjectId

notes = db.notes


class Note:

    @staticmethod
    def add_note(title: str, body: str, user_id: str) -> bool:
        db_response = notes.insert_one({
            'title': title,
            'body': body,
            'user_id': user_id,
            'created_at': datetime.now(),
            'updated_at': None
        })

        return True if db_response else False

    @staticmethod
    def get_note(id: str, user_id: str, needed_attributes: str = ['_id', 'title', 'body', 'user_id', 'created_at', 'updated_at']):
        query = notes.find_one({'_id': ObjectId(id), 'user_id': user_id})
        return Serializer(needed_attributes).serialize(query) if query else {}

    @staticmethod
    def get_notes(user_id: str, needed_attributes: List = ['_id', 'title', 'body', 'user_id', 'created_at', 'updated_at']) -> Dict or List:
        query = notes.find({'user_id': user_id}).sort('_id')

        if query:
            return Serializer(needed_attributes).dump(list(query))
        return {}

    @staticmethod
    def search(user_id: str, search_param: str, needed_attributes=['_id', 'title', 'body', 'user_id', 'created_at', 'updated_at']) -> Dict:
        query = notes.find({
            'user_id': user_id,
            '$or': [{
                'body': {
                    '$regex': search_param,
                    '$options': "i"
                }},
                {'title': {
                    '$regex': search_param,
                    '$options': "i"
                }}
            ]}).sort('_id')

        return Serializer(needed_attributes).dump(list(query)) if query else {}

    @staticmethod
    def __update(id: str, user_id: str, data_to_be_updated: List) -> bool:
        query = notes.update_one({
            '_id': ObjectId(id),
            'user_id': user_id},
            {'$set': {
                data_to_be_updated[0]:data_to_be_updated[1],
                'updated_at':datetime.now()
            }})
        return True if query.modified_count == 1 else False

    @staticmethod
    def update_title(id: str, new_title: str, user_id: str) -> bool:
        return Note.__update(id,user_id,['title',new_title,])

    @staticmethod
    def update_body(id:str,new_body:str,user_id:str) -> bool:
        return Note.__update(id,user_id,['body',new_body])
    
    @staticmethod
    def delete(id:str,user_id:str) -> bool:
        query = notes.find_one_and_delete({'_id':ObjectId(id),'user_id':user_id})
        return True if query else False
