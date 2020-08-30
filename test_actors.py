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

    
    # Actors: helper functions
    def get_mock_actor_from_db(self): 
        url = '/api/actors/search' 
        param = {'name': 'Mock actor name'}

        res = self.client().post(url, json=param)
        actors = json.loads(res.data)["actors"]

        if len(actors) > 0: 
            return actors[0]
        else:
            return None


    def delete_mock_actor_in_db(self):
        actor = self.get_mock_actor_from_db()

        if actor is not None:
            actor_id = actor['id']
            print("Mock actor id: {}".format(actor_id))
            res = self.client().delete('/api/actors/{}'.format(actor_id), headers=self.admin_header)
            return res
        else:
            return None


    def add_mock_actor_to_db(self):
        res = self.client().post('/api/actors/create', json = self.mock_actor, headers=self.admin_header)
        return res


    def add_mock_actor_if_not_exist(self):
        actor = self.get_mock_actor_from_db()

        if actor is None:
            self.add_mock_actor_to_db()


    # Actors: Read - get all
    def test_get_all_actors_ok(self):
        res = self.client().get('/api/actors')
        self.assertEqual(res.status_code, 200)

        data = json.loads(res.data)
        self.assertTrue(len(data['actors'])>0)


    # Actors: Read - search ok
    def test_search_movies_ok(self, json_param=None):
        param = {"name":"Movie"}
        if json_param is not None:
            param = json_param

        res = self.client().post('/api/movies/search', json=param, headers=self.admin_header)
        self.assertEqual(res.status_code, 200)

        data = json.loads(res.data)
        self.assertTrue(len(data['movies'])>0)


    # Actors: Read - search failed
    def test_search_movies_failed(self):
        param = {}
        res = self.client().post('/api/movies/search', json=param)
        self.assertNotEqual(res.status_code, 200)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()