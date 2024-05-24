import re

from flask import jsonify, request

from . import app, db
from .models import URLMap
from .error_handlers import InvalidAPIRequest
from .views import get_unique_short_id


def validate_custom_id(custom_id):
    if len(custom_id) > 16 or not re.match("^[a-zA-Z0-9]*$", custom_id):
        raise InvalidAPIRequest(
            'Указано недопустимое имя для короткой ссылки',
            400
        )
    if URLMap.query.filter_by(short=custom_id).first() is not None:
        raise InvalidAPIRequest(
            'Предложенный вариант короткой ссылки уже существует.'
        )


def get_request_data():
    data = request.get_json()
    if data is None:
        raise InvalidAPIRequest('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIRequest('"url" является обязательным полем!')
    return data


def handle_custom_id(data):
    if 'custom_id' in data and data['custom_id']:
        validate_custom_id(data['custom_id'])
    else:
        data['custom_id'] = get_unique_short_id()


def create_urlap(data):
    url = URLMap()
    url.from_dict(data)
    db.session.add(url)
    db.session.commit()
    return url


@app.route('/api/id/', methods=('POST',))
def create_short_url():
    data = get_request_data()
    handle_custom_id(data)
    url = create_urlap(data)
    return jsonify(
        {
            'short_link': 'http://localhost/' + str(url.short),
            'url': url.original
        }), 201


@app.route('/api/id/<string:short_id>/', methods=('GET',))
def get_short_url(short_id):
    url = URLMap.query.filter_by(short=short_id).first_or_404()
    return jsonify({'url': url.original}), 200