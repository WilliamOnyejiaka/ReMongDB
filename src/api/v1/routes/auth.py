from flask import jsonify,Blueprint,request
from src.config.config import MONGODB_URI
from pymongo import MongoClient
from werkzeug.security import generate_password_hash,check_password_hash

mongo = MongoClient(MONGODB_URI)
db = mongo.remongo_db
users = db.users

auth = Blueprint('auth',__name__,url_prefix="/api/v1/auth")

@auth.get('/sign_up')
def sign_up():
    email = request.get_json().get('email',"email@email.com")
    password = request.get_json().get('password','12345')
    password_hash = generate_password_hash(password)

    db_response = users.insert_one({'email':email,'password':password})
    print(password_hash)
    return jsonify({'email':email,'password':password})