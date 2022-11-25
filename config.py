
TESTING = True
DEBUG = True
FLASK_ENV = "development"
SECRET_KEY = "83278af38b3c630e8774e023bb7d9b77"

TEMPLATES_FOLDER = "templates"
UPLOAD_FOLDER = "uploads"
UPLOAD_FOLDER_FOR_TRANSACTIONS_FILES = f"""{UPLOAD_FOLDER}/transactions_files"""
ALLOWED_EXTENSIONS = {"xlsx", "csv", "SE"}

# Database
SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite3"

