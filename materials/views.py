from materials import app
from .errors import InvalidPOSTData
from .models import add_to_db, search_db
from bson.json_util import dumps
from flask import jsonify, request, Response
from werkzeug.exceptions import BadRequest

@app.route("/")
def home():
    return jsonify('Endpoints: POST /data/add or POST /data/search')

def validate_data(request):
    # Check that post data was json
    try:
        data = request.get_json()
    except BadRequest:
        raise InvalidPOSTData('POST data is not JSON or is improperly formatted')
    if not data:
        raise InvalidPOSTData('Request has no data')
    return data

@app.route("/data/add", methods=["POST"])
def add_data():
    data = validate_data(request)
    # Model code will do error checking that json is properly formatted
    resp, status_code = add_to_db(data)
    # Use dumps instead of jsonify to handle the PyMongo objects
    return Response(dumps(resp), status=status_code, 
               mimetype='application/json')

@app.route("/data/search", methods=["POST"])
def search_data():
    data = validate_data(request)
    resp, status_code = search_db(data)
    return Response(dumps(resp), status=status_code, 
               mimetype='application/json')
