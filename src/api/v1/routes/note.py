from typing import List
from flask import Blueprint,request,jsonify
from flask_jwt_extended import jwt_required,get_jwt_identity
from src.api.v1.models.Note import Note
from src.modules.Serializer import Serializer
from src.modules.Pagination import Pagination


note = Blueprint('note',__name__,url_prefix="/api/v1/note")

@note.post("/add_note")
@jwt_required()
def add_note():
    title = request.get_json().get('title',"")
    body = request.get_json().get('body',"")
    user_id = get_jwt_identity()

    if Note.add_note(title,body,user_id):
        return jsonify({'error':False,'message':"note added successfully"}),201
    return jsonify({'error':True,'message':"something went wrong"}),500

@note.get("/get_note/<id>")
@jwt_required()
def get_note(id:str):
    user_id = get_jwt_identity()
    user_notes = Note.get_note(id,user_id)
    return jsonify({'error':False,'message':user_notes}),200

@note.get("/get_notes")
@jwt_required()
def get_notes():
    user_id = get_jwt_identity()
    user_notes = Note.get_notes(user_id)
    return jsonify({'error':False,'data':user_notes}),200

@note.get("/pagination/note_pagination")
@jwt_required()
def note_pagination():
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit',10))
    except:
        return jsonify({'error':True,'message':"page and limit must be integers"}),400
    
    user_id = get_jwt_identity()
    pagination_results = Pagination(Note.get_notes(user_id),page,limit).meta_data()
    return jsonify({'error':False,'data':pagination_results}),200
    

@note.get("/search/<search_param>")
@jwt_required()
def search(search_param):
    user_id = get_jwt_identity()
    search_results:List = Note.search(user_id,search_param)
    return jsonify({'error':False,'data':search_results}),200

