from flask import jsonify, render_template, request

from . import app, db


class InvalidAPIRequest(Exception):

    def __init__(self, message, status_code=400):
        super().__init__()
        self.message = message
        if status_code:
            self.status_code = status_code

    def to_dict(self):
        return {'message': self.message}


@app.errorhandler(InvalidAPIRequest)
def invalid_api_request(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.errorhandler(404)
def page_not_found(error):
    if request.path.startswith('/api/'):
        return jsonify({'message': 'Указанный id не найден'}), 404
    else:
        return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
