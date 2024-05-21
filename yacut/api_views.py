from flask import jsonify, request

from . import app, db
from .models import URLMap
from .error_handlers import InvalidAPIRequest


@app.route('/api/id/', methods=['POST'])
def create_short_url():
    data = request.get_json()
    if data is None or 'original' not in data:
        raise InvalidAPIRequest('В запросе отсутствуют обязательные поля')
    if 'short' in data:
        if len(data['short']) >= 16:
            raise InvalidAPIRequest(
                'Длина идентификатора превышает 16 символов'
            )
        if URLMap.query.filter_by(short=data['short']).first() is not None:
            raise InvalidAPIRequest('Такое мнение уже есть в базе данных')
    url_m = URLMap()
    url_m.from_dict(data)
    db.session.add(url_m)
    db.session.commit()
    return jsonify({'url': url_m.to_dict()}), 201


@app.route('/api/id/<string:short_id>', methods=['GET'])
def get_short_url(short_id):
    url_m = URLMap.query.filter_by(short=short_id).first()
    if url_m is None:
        raise InvalidAPIRequest('Мнение с указанным short_id не найдено', 404)
    return jsonify({'url': url_m.to_dict()}), 200