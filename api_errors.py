from flask import Blueprint, jsonify
from flask_api import status
from werkzeug.exceptions import HTTPException

errors = Blueprint('errors', __name__)

@errors.app_errorhandler(HTTPException)
def http_error(e):
    return jsonify(error=str(e)), e.code

@errors.app_errorhandler(Exception)
def error_handler(e):
    print(e)
    return jsonify(error=str(e)), status.HTTP_400_BAD_REQUEST