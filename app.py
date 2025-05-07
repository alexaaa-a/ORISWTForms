from flask import Flask, render_template
from flask_migrate import Migrate
from flask_restful import Api
from models import db
from resources import SeriesListResource, SeriesResource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

api.add_resource(SeriesListResource, '/api/series')
api.add_resource(SeriesResource, '/api/series/<int:series_id>')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)