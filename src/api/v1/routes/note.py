from email import message
from flask import Blueprint,request,jsonify
from flask_jwt_extended import jwt_required,get_jwt_identity
from src.api.v1.models.Note import Note
from src.modules.Serializer import Serializer


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
    return jsonify({'error':True,'message':user_notes}),200


