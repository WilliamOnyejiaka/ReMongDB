from typing import List,Dict
from flask import Blueprint,request,jsonify
from flask_jwt_extended import jwt_required,get_jwt_identity
import jwt
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
    return jsonify({'error':False,'data':user_notes}),200

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

@note.get("/pagination/search_pagination/<search_param>")
@jwt_required()
def search_pagination(search_param):
    user_id = get_jwt_identity()
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
    except:
        return jsonify({'error':True,'message':"page and limit must be integers"}),400

    pagination_results:Dict = Pagination(Note.search(user_id,search_param),page,limit).meta_data()
    return jsonify({'error':False,'data':pagination_results}),200

@note.patch("/update/title/<id>")
@jwt_required()
def update_title(id):
    user_id = get_jwt_identity()
    new_title = request.get_json().get('new_title',None)

    if not new_title:
        return jsonify({'error':True,'message':"new_title needed"}),400
    
    if Note.update_title(id, new_title, user_id):
        return jsonify({'error':False,'message':"note has been updated successfully"}),200
    return jsonify({'error':True,'message':"something went wrong"}),500

@note.patch("/update/body/<id>")
@jwt_required()
def update_body(id):
    user_id = get_jwt_identity()
    new_body = request.get_json().get('new_body',None)

    if not new_body:
        return jsonify({'error':True,'message':"new_body needed"}),400
    
    if Note.update_body(id,new_body,user_id):
        return jsonify({'error':False,'message':"note body updated successfully"}),200
    return jsonify({'error':True,'message':"something went wrong"}),500

@note.delete("/delete/<id>")
@jwt_required()
def delete(id):
    user_id = get_jwt_identity()
    if not Note.get_note(id,user_id):
        return jsonify({'error':True,'message':"note does not exist"}),400
    
    if Note.delete(id,user_id):
        return jsonify({'error':False,'message':"note deleted successfully"}),200
    return jsonify({'error':True,'message':"something went wrong"}),500