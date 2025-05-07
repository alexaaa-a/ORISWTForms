from flask_marshmallow import Marshmallow
from flask_restful import Resource
from marshmallow import Schema, fields as ma_fields, ValidationError
from models import Series, db
from flask import request

ma = Marshmallow()


class SeriesSchema(ma.Schema):
    id = ma_fields.Integer(dump_only=True)
    name = ma_fields.String(required=True)
    description = ma_fields.String(required=True)


series_schema = SeriesSchema()
series_list_schema = SeriesSchema(many=True)


class SeriesResource(Resource):
    def get(self, series_id):
        query = Series.query.where(Series.id == series_id)
        series = db.session.execute(query).scalar()
        if series:
            return series_schema.dump(series)
        return {"error": "Series not found"}, 404

    def patch(self, series_id):
        query = Series.query.where(Series.id == series_id)
        series = db.session.execute(query).scalar()
        if series:
            if name := request.json.get("name"):
                series.name = name
            if description := request.json.get("description"):
                series.description = description
            db.session.commit()
            return {"message": "Series updated successfully"}
        return {"error": "Series not found"}, 404

    def delete(self, series_id):
        query = Series.query.where(Series.id == series_id)
        series = db.session.execute(query).scalar()
        if series:
            db.session.delete(series)
            db.session.commit()
            return {"message": "Series deleted successfully"}
        return {"error": "Series not found"}, 404


class SeriesListResource(Resource):
    def get(self):
        series = Series.query.all()
        return series_list_schema.dump(series)

    def post(self):
        data = request.json
        if not data:
            return {"error": "No input data provided"}, 400

        try:
            new_series = series_schema.load(data)
        except ValidationError as err:
            return {"errors": err.messages}, 400

        series = Series(name=new_series['name'], description=new_series['description'])
        db.session.add(series)
        db.session.commit()
        return series_schema.dump(series), 201