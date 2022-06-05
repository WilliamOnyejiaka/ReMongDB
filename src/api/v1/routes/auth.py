from flask import jsonify,Blueprint,request
import validators
from src.api.v1.models.User import User
from werkzeug.security import check_password_hash
from flask_jwt_extended import get_jwt_identity,create_access_token,create_refresh_token,jwt_required

auth = Blueprint('auth',__name__,url_prefix="/api/v1/auth")

@auth.post("/sign_up")
def sign_up():
    name = request.get_json().get('name',None)
    email = request.get_json().get('email',None)
    password = request.get_json().get('password',None)

    if not name:
        return jsonify({'error':True,'message':"name needed"}),400
    if not email:
        return jsonify({'error': True, 'message': "email needed"}),400
    if not password:
        return jsonify({'error': True, 'message': "password needed"}),400
    if len(name) < 2:
        return jsonify({'error': True, 'message': "name length should be greater than 1"}),400
    if len(password) < 5:
        return jsonify({'error':True,'message':"password length should be greater than 4"}),400
    if not validators.email(email):
        return jsonify({'error':True,'message':"valid email needed"}),400
    if (User.get_user_with_email(email)):
        return jsonify({'error':True,'message':"email already exits"}),400
    
    if User.create_user(name,email,password):
        return jsonify({'error':False,'message':"user created successfully"}),201

    return jsonify({'error':True,'message':"something went wrong"}),500

@auth.get("/login")
def login():
    email = request.authorization.get('username',None)
    password = request.authorization.get('password',None)

    if not email:
        return jsonify({'error':True,'message':"email needed"}),400
    if not password:
        return jsonify({'error':True,'message':"password needed"}),400

    user = User.get_user_with_email(email)

    if user:
        if check_password_hash(user['password'],password):
            access_token = create_access_token(identity=user['_id'])
            refresh_token = create_refresh_token(identity=user['_id'])

            return jsonify({
                'error':False,
                'data': User.get_user_with_email(email,['_id','name','email','created_at','updated_at']),
                'tokens':{
                    'access_token':access_token,
                    'refresh_token':refresh_token
                }
            }),200

        return jsonify({'error':True,'error':"invalid credentials"}),400
    
    return jsonify({'error':True,'message':"invalid credentials"}),400

@auth.get("/token/new_access_token")
@jwt_required(refresh=True)
def new_access_token():
    user_id = get_jwt_identity()
    access_token = create_access_token(identity=user_id)
    return jsonify({'access_token':access_token}),201

@auth.delete("/delete")
@jwt_required()
def delete():
    user_id = get_jwt_identity()

    if not User.get_user_with_id(user_id):
        return jsonify({'error':True,'message':"user does not exists"}),400
    
    if User.delete(user_id):
        return jsonify({'error':False,'message':"user deleted successfully"}),200
    return  jsonify({'error':True,'message':"something went wrong"}),500