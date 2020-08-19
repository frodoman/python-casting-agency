from sqlalchemy import Table, Column, create_engine, Float, Integer, String, MetaData, ForeignKey
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import json
import os


#database_path = os.environ['SQLALCHEMY_DATABASE_URI']
#os.environ['DATABASE_URL']
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

'''
Movie
Have title and release year
'''
class Movie(db.Model):  
  __tablename__ = 'movie'

  id = Column(Integer, primary_key=True)
  title = Column(String)

  def __init__(self, title):
    self.title = title

  def format(self):
    return {
      'id': self.id,
      'title': self.title }