from flask import Flask
from flask_migrate import Migrate

from models import db, create_table
from views import SeriesView, SeriesList, SeriesCreate, SeriesUpdate, SeriesDelete
import os

app = Flask(__name__, template_folder=os.path.abspath('templates'))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
app.config['SECRET_KEY'] = os.urandom(24)
db.init_app(app)

migrate = Migrate(app, db)

create_table(app)

app.add_url_rule('/', view_func=SeriesList.as_view('series.list', engine=db))
app.add_url_rule('/series/<string:series_id>/', view_func=SeriesView.as_view('series.view', engine=db))
app.add_url_rule('/series/create/', view_func=SeriesCreate.as_view('series.create', engine=db))
app.add_url_rule('/series/<string:series_id>/update/', view_func=SeriesUpdate.as_view('series.update', engine=db))
app.add_url_rule('/series/<string:series_id>/delete/', view_func=SeriesDelete.as_view('series.delete', engine=db))

if __name__ == "__main__":
    app.run(debug=True)