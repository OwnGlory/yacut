import random
import string
from flask import flash, render_template, redirect, url_for, abort

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
            while URLMap.query.filter_by(
                short=short_link
            ).first() is not None:
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
    else:
        print(form.errors)
    return render_template('main.html', form=form)


def get_unique_short_id(length=6):
    id = ''.join(
        random.choice(
            string.ascii_letters + string.digits
        ) for _ in range(length))
    return id


@app.route('/<short_id>')
def redirect_to_url(short_id):
    urlmap = URLMap.query.filter_by(short=short_id).first()
    if urlmap:
        return redirect(urlmap.original)
    else:
        abort(404)
