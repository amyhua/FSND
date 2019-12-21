from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
db = SQLAlchemy()

# Set up my Database
def setup_db(app):
    app.config.from_object('config')
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)
    return db

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500), nullable=False)
    website = db.Column(db.String(), nullable=True)
    facebook_link = db.Column(db.String(120), nullable=True)
    seeking_talent = db.Column(db.Boolean, nullable=False, default=True)
    seeking_description = db.Column(db.String(120), nullable=True)
    shows = db.relationship('Show', backref='venue', lazy=True)


    @property
    def city_and_state(self):
      return { 'city': self.city, 'state': self.state }

    @property
    def all_about_shows(self):
      past_shows = venue_past_shows(self.id)
      upcoming_shows = venue_upcoming_shows(self.id)

      return {
        'id': self.id,
        'name': self.name,
        'address': self.address,
        'city': self.city,
        'state': self.state,
        'phone': self.phone,
        'website': self.website,
        'facebook_link': self.facebook_link,
        'seeking_talent': self.seeking_talent,
        'seeking_description': self.seeking_description,
        'image_link': self.image_link,
        'past_shows': [{
          'artist_id': p.artist_id,
          'artist_name': p.artist.name,
          'artist_image_link': p.artist.image_link,
          'start_time': p.start_time.strftime("%m/%d/%Y, %H:%M")
          } for p in past_shows],
          'upcoming_shows': [{
              'artist_id': u.artist.id,
              'artist_name': u.artist.name,
              'artist_image_link': u.artist.image_link,
              'start_time': u.start_time.strftime("%m/%d/%Y, %H:%M")
          } for u in upcoming_shows],
          'past_shows_count': len(past_shows),
          'upcoming_shows_count': len(upcoming_shows)
      }


class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.ARRAY(db.String()), nullable=False)
    image_link = db.Column(db.String(500), nullable=False)
    website = db.Column(db.String(), nullable=True)
    facebook_link = db.Column(db.String(120), nullable=True)
    seeking_venue = db.Column(db.Boolean, nullable=False, default=True)
    seeking_description = db.Column(db.String(120), nullable=True)
    shows = db.relationship('Show', backref='artist', lazy=True)


    @property
    def basic_details(self):
      return { 'id': self.id, 'name': self.name }

    @property
    def all_about_shows(self):
      past_shows = artist_past_shows(self.id)
      upcoming_shows = artist_upcoming_shows(self.id)

      return {
        'id': self.id,
        'name': self.name,
        'city': self.city,
        'state': self.state,
        'phone': self.phone,
        'genres': self.genres,
        'website': self.website,
        'facebook_link': self.facebook_link,
        'seeking_venue': self.seeking_venue,
        'seeking_description': self.seeking_description,
        'image_link': self.image_link,
        'past_shows': [{
          'venue_id': past.venue_id,
          'venue_name': past.venue.name,
          'venue_image_link': past.venue.image_link,
          'start_time': past.start_time.strftime("%m/%d/%Y, %H:%M")
          } for past in past_shows],
        'upcoming_shows': [{
            'venue_id': upcoming.venue.id,
            'venue_name': upcoming.venue.name,
            'venue_image_link': upcoming.venue.image_link,
            'start_time': upcoming.start_time.strftime("%m/%d/%Y, %H:%M")
        } for upcoming in upcoming_shows],
        'past_shows_count': len(past_shows),
        'upcoming_shows_count': len(upcoming_shows)
      }


class Show(db.Model):
    __tablename__ = 'shows'

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime())
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'))
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'))

    @property
    def upcoming(self):
      venue = get_venue(self.venue_id)
      artist = get_artist(self.artist_id)

      if self.start_time > datetime.now():
        return {
          "venue_id": self.venue_id,
          "venue_name": venue.name,
          "artist_id": self.artist_id,
          "artist_name": artist.name,
          "artist_image_link": artist.image_link,
          "start_time": self.start_time.strftime("%m/%d/%Y, %H:%M")
        }
      else:
        return None


# Defines
def get_venue(venue_id):
  return Venue.query.get(venue_id)

def get_artist(artist_id):
  return Artist.query.get(artist_id)

def venue_past_shows(venue_id):
  return Show.query.filter(Show.start_time < datetime.now(), Show.venue_id == venue_id).all()

def venue_upcoming_shows(venue_id):
  return Show.query.filter(Show.start_time > datetime.now(), Show.venue_id == venue_id).all()

def artist_past_shows(artist_id):
  return Show.query.filter(Show.start_time < datetime.now(), Show.artist_id == artist_id).all()

def artist_upcoming_shows(artist_id):
  return Show.query.filter(Show.start_time > datetime.now(), Show.artist_id == artist_id).all()
