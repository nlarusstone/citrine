from flask import make_response, jsonify
from materials import app

class InvalidPOSTData(Exception):
    status_code = 400

    def __init__(self, message, status_code=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        except_dict = {'message': self.message}
        return except_dict

@app.errorhandler(InvalidPOSTData)
def handle_invalid_post_data(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.errorhandler(400)
def bad_request(message=None):
    err = {'error': 'Bad request', 'message': message}
    return make_response(jsonify(err), 400)

@app.errorhandler(404)
def not_found(message=None):
    err = {'error': 'Not found', 'message': message}
    return make_response(jsonify(err), 404)


