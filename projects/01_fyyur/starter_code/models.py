from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime


db = SQLAlchemy()
# Set up my Database
def setup_db(app):
    app.config.from_object('config')
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)
    return db

# Columns upon gaven Data
class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    website = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.String(120), nullable=True)
    seeking_talent = db.Column(db.Boolean, nullable=True)
    seeking_description = db.Column(db.String(500), nullable=True)
    image_link = db.Column(db.String(500), nullable=True)
    facebook_link = db.Column(db.String(120), nullable=True)
    shows = db.relationship('Show', backref='Venue', lazy=True)

# TODO: implement any missing fields, as a database migration using Flask-Migrate
# properties
    # Upcoming Shows property
    @property
    def upcoming_shows(self):
      now = datetime.now()
      upcoming_shows = [show for show in self.shows if show.start_time > now]
      return upcoming_shows

    # Past Shows property
    @property
    def past_shows(self):
      past_shows = [show for show in self.shows if show.start_time < datetime.now()]
      return past_shows

    # Number of Upcoming Shows property
    @property
    def num_upcoming_shows(self):
      return len(self.upcoming_shows)

    # Number of Past Shows property
    @property
    def num_past_shows(self):
      return len(self.past_shows)


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    website = db.Column(db.String(500))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(500), nullable=True)
    shows = db.relationship('Show', backref='Artist', lazy=True)

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    # Upcoming Shows property
    @property
    def upcoming_shows(self):
      now = datetime.now()
      upcoming_shows = [show for show in self.shows if show.start_time > now]
      return upcoming_shows

    @property
    def num_upcoming_shows(self):
      upcoming_shows = [show for show in self.shows if show.start_time < datetime.now()]
      return len(upcoming_shows)

    # Past Shows property
    @property
    def past_shows(self):
      past_shows = [show for show in self.shows if show.start_time < datetime.now()]
      return past_shows

    # Number of Upcoming Shows property
    @property
    def num_upcoming_shows(self):
      return len(self.upcoming_shows)

    # Number of Past Shows property
    @property
    def num_past_shows(self):
      return len(self.past_shows)

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)
