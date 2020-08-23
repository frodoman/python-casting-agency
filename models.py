from sqlalchemy import Table, Column, create_engine, Float, Integer, String, MetaData, ForeignKey
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import json
import os
from helper import *


database_name = "casting_agency_app"
local_db_path = "postgres://{}/{}".format('XinghouLiu@localhost:5432', database_name)
db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()
'''

def set_up_db(app):
    app.config.from_object('config')
    if app.debug: 
      app.config['SQLALCHEMY_DATABASE_URI'] = local_db_path

    if 'DATABASE_URL' in os.environ:
      app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

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
    return {
      'id': self.id,
      'title': self.title, 
      'release_date':  dateTimeToString(self.release_date)}
