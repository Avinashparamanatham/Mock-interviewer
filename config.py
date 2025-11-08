import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_very_secret_key_that_should_be_changed'
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    # Configuration for Flask-SocketIO
    SECRET_KEY_SOCKET = os.environ.get('SECRET_KEY_SOCKET') or 'another_secret_key'
    # Directory for temporary audio and image files
    UPLOAD_FOLDER = 'static/temp_uploads'
    
    # Ensure upload folder exists
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)