import flask
import json
from flask import request, jsonify
from flask_api import status
from app.recommendation.recommendation import recommend
from api_errors import errors

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.register_blueprint(errors)

@app.route('/')
def ping():
    return json.dumps({'success':True}), 200, {'Content-type':'application/json'}

@app.route('/<cliente>', methods=['GET'])
def recommendation(cliente):
    return {
        'cliente': cliente,
        'recommendations': recommend(cliente)
    }, status.HTTP_200_OK

if __name__ == "__main__":
    app.run()