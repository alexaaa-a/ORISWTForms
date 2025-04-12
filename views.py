from flask import request, url_for, render_template, redirect, flash
from flask.views import MethodView
from flask_sqlalchemy import SQLAlchemy

from forms import SeriesDeleteForm, SeriesUpdateForm, SeriesCreateForm
from models import Series


class SeriesList(MethodView):
    init_every_request = False

    def __init__(self, engine: SQLAlchemy):
        self.engine = engine

    def get(self):
        series: list[Series] = self.engine.session.execute(Series.query).scalars()
        return render_template('series/list.html', series=series)


class SeriesView(MethodView):
    init_every_request = False

    def __init__(self, engine: SQLAlchemy):
        self.engine = engine

    def get(self, series_id: str):
        query = Series.query.where(Series.id == series_id)
        series: Series = self.engine.session.execute(query).scalar()
        if not series:
            return 'Not found'
        return render_template('series/read.html', series=series)


class SeriesUpdate(MethodView):
    init_every_request = False

    def __init__(self, engine: SQLAlchemy):
        self.engine = engine

    def get(self, series_id: str):
        query = Series.query.where(Series.id == series_id)
        series: Series = self.engine.session.execute(query).scalar()
        if not series:
            return 'Not found'
        form = SeriesUpdateForm(
            name=series.title,
            description=series.description,
        )
        return render_template('series/update.html', series=series, form=form)

    def post(self, series_id: str):
        query = Series.query.where(Series.id == series_id)
        series: Series = self.engine.session.execute(query).scalar()
        if not series:
            return 'Not found'

        form = SeriesUpdateForm(request.form)
        if form.validate():
            series.title = form.title.data
            series.description = form.description.data
            self.engine.session.commit()

        return redirect(url_for('series.list', series_id=series.id))


class SeriesDelete(MethodView):
    init_every_request = False

    def __init__(self, engine: SQLAlchemy):
        self.engine = engine

    def get(self, series_id: str):
        query = Series.query.where(Series.id == series_id)
        series: Series = self.engine.session.execute(query).scalar()
        if not series:
            return 'Not found'
        form = SeriesDeleteForm()
        return render_template('series/delete.html', series=series, form=form)

    def post(self, series_id: str):
        query = Series.query.where(Series.id == series_id)
        series: Series = self.engine.session.execute(query).scalar()
        if not series:
            return 'Not found'
        form = SeriesDeleteForm(request.form)
        if form.validate():
            self.engine.session.delete(series)
            self.engine.session.commit()

        return redirect(url_for('series.list'))


class SeriesCreate(MethodView):
    init_every_request = False

    def __init__(self, engine: SQLAlchemy):
        self.engine = engine

    def get(self):
        form = SeriesCreateForm()
        return render_template('series/create.html', form=form)

    def post(self):
        form = SeriesCreateForm(request.form)
        if form.validate():
            series = Series(
                title=form.title.data,
                description=form.description.data
            )

            self.engine.session.add(series)
            self.engine.session.commit()
            flash("Success!", category='success')
        else:
            flash("Error", category='error')

        return redirect(url_for('series.list'))