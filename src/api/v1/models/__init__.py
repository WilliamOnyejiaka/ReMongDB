from pymongo import MongoClient
from src.config import MONGODB_URI

mongodb = MongoClient(MONGODB_URI)
db = mongodb.remongo_db