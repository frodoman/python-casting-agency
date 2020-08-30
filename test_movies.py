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
        #setup_test_case(test=self)
        super().setUp()

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()


    def tearDown(self):
        """Executed after reach test"""
        self.delete_mock_movie_in_db()
        pass

    
    # Movies: Create - ok
    def test_create_one_movie_ok(self):
        self.delete_mock_movie_in_db()

        res = self.add_mock_movie_to_db()
        self.assertEqual(res.status_code, 200)


    # Movies: Create - faliure
    def test_create_one_movie_failed(self):
        url = '/api/movies/create'

        # not authorized
        res = self.client().post(url, json = self.mock_movie)
        self.assertNotEqual(res.status_code, 200)
        self.assertEqual(res.status_code, 401)

        # not allowed for manager 
        res = self.client().post(url, json=self.mock_movie, headers=self.manager_header)
        self.assertEquals(res.status_code, 403)

        # not allowed for user
        res = self.client().post(url, json=self.mock_movie, headers=self.user_header)
        self.assertEquals(res.status_code, 403)


    # Movies: Read - get all
    def test_get_all_movies(self):
        res = self.client().get('/api/movies')
        self.assertEqual(res.status_code, 200)

        data = json.loads(res.data)
        self.assertTrue(len(data['movies'])>0)


    # Movies: Read - search ok
    def test_search_movies_ok(self, json_param=None):
        param = {"title":"Movie"}
        if json_param is not None:
            param = json_param

        res = self.client().post('/api/movies/search', json=param, headers=self.admin_header)
        self.assertEqual(res.status_code, 200)

        data = json.loads(res.data)
        self.assertTrue(len(data['movies'])>0)


    # Movies: Read - search failed
    def test_search_movies_failed(self):
        param = {}
        res = self.client().post('/api/movies/search', json=param)
        self.assertNotEqual(res.status_code, 200)


    # Movies: Update - ok
    def test_update_movie_ok(self):
        self.add_mock_movie_if_not_exist()
        movie = self.get_mock_movie_from_db()
        
        movie['title'] = "Mock movie title - Updated!"
        movie_id = movie['id']

        # Role: admin - ok
        res = self.client().patch('/api/movies/{}'.format(movie_id), json=movie, headers=self.admin_header)
        self.assertEquals(res.status_code, 200)

        # Role: manager - ok
        res = self.client().patch('/api/movies/{}'.format(movie_id), json=movie, headers=self.manager_header)
        self.assertEquals(res.status_code, 200)

        self.test_search_movies_ok(json_param = {"title":"title - Updated"})
        self.delete_mock_movie_in_db()


    # Movies: Update - failed
    def test_update_movie_failed(self):
        self.add_mock_movie_if_not_exist()
        movie = self.get_mock_movie_from_db()
        
        movie['title'] = "Mock movie title - Updated!"
        movie_id = movie['id']
        url = '/api/movies/{}'.format(movie_id)

        # Missing json data
        res = self.client().patch(url, json=None, headers = self.admin_header)
        self.assertEquals(res.status_code, 422)

        # Role: user - not allowed
        res = self.client().patch(url, json=movie_id, headers = self.user_header)
        self.assertEquals(res.status_code, 403)
        self.delete_mock_movie_in_db()


    # Movies: Delete - ok
    def test_delete_movie_ok(self):
        self.add_mock_movie_if_not_exist()
        movie = self.get_mock_movie_from_db()

        movie_id = movie['id']
        url = '/api/movies/{}'.format(movie_id)

        # Role: Admin - ok
        res = self.client().delete(url, headers = self.admin_header)
        self.assertEquals(res.status_code, 200)

        # Should not found it by id
        res = self.client().get(url, headers = self.admin_header)
        self.assertEquals(res.status_code, 404)

        self.delete_mock_movie_in_db()

    # Movies: Delete - failed
    def test_delete_movie_failed(self):
        self.add_mock_movie_if_not_exist()
        movie = self.get_mock_movie_from_db()

        movie_id = movie['id']
        url = '/api/movies/{}'.format(movie_id)

        # Role: manager - not allowed
        res = self.client().delete(url, headers = self.manager_header)
        self.assertEquals(res.status_code, 403)

        # Role: user - failed
        res = self.client().delete(url, headers = self.user_header)
        self.assertEquals(res.status_code, 403)

        self.delete_mock_movie_in_db()

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()