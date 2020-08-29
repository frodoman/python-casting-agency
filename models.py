from sqlalchemy import Table, Column, create_engine, Float, Integer, String, MetaData, ForeignKey
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import json
import os
from helper import *
from consts import *

database_name = "casting_agency_app"
local_db_path = "postgres://{}/{}".format('XinghouLiu@localhost:5432', database_name)
db = SQLAlchemy()


def set_up_db(app, db_path=None):
    app.config.from_object('config')
    db_path_key = 'SQLALCHEMY_DATABASE_URI'
    if app.debug: 
      app.config[db_path_key] = local_db_path

    if KEY_DB_URL in os.environ:
      app.config[db_path_key] = os.environ[KEY_DB_URL]

    if db_path is not None: 
      app.config[db_path_key] = db_path

    db.app = app
    db.init_app(app)


class Actors(db.Model):
  __tablename__ = 'Actors'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  age = db.Column(db.Integer)
  gender = db.Column(db.String)

  def __init_(self, name, age, gender):
    self.name = name
    self.age = age
    self.gender = gender
  
  def format(self):
    return {
      'id': self.id, 
      'name': self.name,
      'age': self.age,
      'gender': self.gender
    }

  @staticmethod
  def is_valide_payload(payload: dict):
    if 'name' not in payload or 'age' not in payload or 'gender' not in payload:
      return False
    else:
      return True


#  ----------------------------------------------------------------  
#  Reference table between Movie and Actor, 
#  which is Many to Many relationship
#  ----------------------------------------------------------------  


movie_actor = db.Table('movie_actor', 
    db.Column('movie_id', db.Integer, db.ForeignKey('Movies.id'), primary_key=True),
    db.Column('actor_id', db.Integer, db.ForeignKey('Actors.id'), primary_key=True)
)


'''
Movie
Have title and release year
'''
class Movies(db.Model):  
  __tablename__ = 'Movies'

  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String)
  release_date = db.Column(db.DateTime)
  actors = db.relationship('Actors', secondary=movie_actor, backref=db.backref('movies', lazy=True))

  def __init__(self, title, release_date):
    self.title = title
    self.release_date = release_date

  def format(self):
    actor_ids = []
    if len(self.actors) > 0:
      actor_ids = [actor.id for actor in self.actors]

    return {
      'id': self.id,
      'title': self.title, 
      'release_date':  dateTimeToString(self.release_date), 
      'actors': actor_ids}

  @staticmethod
  def is_valide_payload(payload: dict):
    if payload is None: 
      return False
    elif 'title' not in payload or 'release_date' not in payload:
      return False
    else:
      return True