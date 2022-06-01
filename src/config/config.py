from dotenv import load_dotenv
import os
load_dotenv()

SECRET_KEY=os.environ.get('SECRET_KEY')
JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY')
MONGODB_URI=os.environ.get('MONGODB_URI')