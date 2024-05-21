from flask_wtf import FlaskForm
from wtforms import URLField, StringField
from wtforms.validators import DataRequired, Length, Optional


class URLForm(FlaskForm):
    original_link = URLField(
        'Введите полную ссылку',
        validators=(DataRequired(message='Обязательное поле'),)
    )
    custom_id = StringField(
        'Введите желаемый идентификатор',
        validators=(
            Length(1, 16, message='Длина ссылки не более 16 символов'),
            Optional()
        )
    )
