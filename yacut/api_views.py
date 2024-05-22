import re
# from http import HTTPStatus
from flask import jsonify, request

from . import app, db
from .models import URLMap
from .error_handlers import InvalidAPIRequest
from .views import get_unique_short_id


@app.route('/api/id/', methods=['POST'])
def create_short_url():
    data = request.get_json()
    if data is None:
        raise InvalidAPIRequest('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIRequest('"url" является обязательным полем!')
    if 'custom_id' in data and data['custom_id']:
        if (
            len(data['custom_id']) > 16 or
            not re.match("^[a-zA-Z0-9]*$", data['custom_id'])
        ):
            raise InvalidAPIRequest(
                'Указано недопустимое имя для короткой ссылки',
                400
            )
        if URLMap.query.filter_by(short=data['custom_id']).first() is not None:
            raise InvalidAPIRequest(
                'Предложенный вариант короткой ссылки уже существует.'
            )
    else:
        data['custom_id'] = get_unique_short_id()
    url_m = URLMap()
    url_m.from_dict(data)
    db.session.add(url_m)
    db.session.commit()
    return jsonify(
        {
            'short_link': 'http://localhost/' + str(url_m.short),
            'url': url_m.original
        }), 201


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_short_url(short_id):
    url_m = URLMap.query.filter_by(short=short_id).first()
    if url_m is None:
        raise InvalidAPIRequest('Указанный id не найден', 404)
    return jsonify({'url': url_m.original}), 200