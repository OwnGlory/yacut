import random
import string

from flask import flash, render_template, redirect, url_for

from . import app, db
from .forms import URLForm
from .models import URLMap


@app.route('/', methods=('GET', 'POST'))
def index_view():
    form = URLForm()
    if form.validate_on_submit():
        short_link = form.custom_id.data
        if URLMap.query.filter_by(
            short=short_link
        ).first() is not None:
            flash('Предложенный вариант короткой ссылки уже существует.')
            return render_template('main.html', form=form)
        if not short_link:
            short_link = get_unique_short_id()

        urlmap = URLMap(
            original=form.original_link.data,
            short=short_link
        )
        db.session.add(urlmap)
        db.session.commit()
        new_link = url_for(
            "redirect_to_url",
            short_id=short_link,
            _external=True
        )
        flash(
            'Ваша новая ссылка готова: <a href="{}">{}</a>'.format(
                new_link,
                new_link
            ), 'safe'
        )
    return render_template('main.html', form=form)


def get_unique_short_id(length=6):
    while True:
        id = ''.join(
            random.choice(
                string.ascii_letters + string.digits
            ) for _ in range(length))
        if URLMap.query.filter_by(short=id).first() is None:
            return id


@app.route('/<string:short_id>')
def redirect_to_url(short_id):
    urlmap = URLMap.query.filter_by(short=short_id).first_or_404()
    return redirect(urlmap.original)
