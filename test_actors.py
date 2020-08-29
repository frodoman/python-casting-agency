import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from models import *
from sqlalchemy import Table, Column, create_engine, Float, Integer, String, MetaData, ForeignKey
from flask_sqlalchemy import SQLAlchemy
from test_commons import *


class MovieTest(BaseTest):
        
    def setUp(self):
        """Define test variables and initialize app."""
        super().setUp()

        self.mock_movie = {
            'title':'Movie Title Mock',
            'release_date': "2020-10-10"
        }

        self.mock_actor = {
            'name': 'Mock actor name',
            'gender': 'M', 
            'age': 22
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()


    def tearDown(self):
        """Executed after reach test"""
        pass


    # Actors: get all
    def test_get_all_actors_ok(self):
        res = self.client().get('/api/actors')
        self.assertEqual(res.status_code, 200)

        data = json.loads(res.data)
        self.assertTrue(len(data['actors'])>0)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()