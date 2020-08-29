import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from casting_agency_app import *
from models import *
from sqlalchemy import Table, Column, create_engine, Float, Integer, String, MetaData, ForeignKey
from flask_sqlalchemy import SQLAlchemy

JWT_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkE4UUw4Qy00Y0RoWG5iTlhIS3lJSiJ9.eyJpc3MiOiJodHRwczovL2NvZmZlZS14LmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjNmZjI0MDE3MDRhZjAwNmRlNzAwY2QiLCJhdWQiOiJjYXN0aW5nLWFnZW5jeSIsImlhdCI6MTU5ODcxMTM4NiwiZXhwIjoxNTk4NzE4NTg2LCJhenAiOiJycldqWjViM0VnSlBSV3VZaUVJTEo2azFnZVJuc01iaSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIiwicmVhZDphY3RvcnMiLCJyZWFkOm1vdmllcyJdfQ.VAyuvvvB_2J4UjgBxmGnIj3V8HS5UnUZoYxpDIJJPqgBoaJKVHY6g1XTqGrj5iW-O9irHgzNG8cQG243hdd9Qppv127FAhCjzV7YrZkbUwekWhO14uZO28slR6HEIJt4_9Tof3WYob0Zbb29PfwneSCkvf0ytS7XN5-D2XPaJPmKsTH4zmSPozWblwx4n4P5i7ZfGADkgGOypP4zqqr2qCuvarAIIAke8EXI-fxV4ucbSOBjUvGR69wr_SAkOq0m0og47DXScS36gXhItMJhJvwK5hMDR6MoXhQh9m9Z7RfS_C-4zHnA9EFZjWdO5uGJf_DfJ_qU3lbaosDOX4NK4Q'

class CastingAgencyTest(unittest.TestCase):
    
    
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "casting_agency_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name) 
        
        set_up_db(self.app, self.database_path)

        self.mock_movie = {
            'title':'Movie Title Mock',
            'release_date': "2020-10-10"
        }

        self.mock_actor = {
            'name': 'Mock actor name',
            'gender': 'M', 
            'age': 22
        }

        self.request_header = {'Authorization': 'Bearer ' + JWT_TOKEN}
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()


    def tearDown(self):
        """Executed after reach test"""
        pass


    # Movies: test get all
    def test_get_all_movies(self):
        res = self.client().get('/api/movies')
        self.assertEqual(res.status_code, 200)

        data = json.loads(res.data)
        self.assertTrue(len(data['movies'])>0)

    # Movies: test create/add
    def test_create_one_movie_ok(self):
        res = self.client().post('/api/movies/create', json = self.mock_movie, headers=self.request_header)
        self.assertEqual(res.status_code, 200)


    def test_create_one_movie_failed(self):
        res = self.client().post('/api/movies/create', json = self.mock_movie)
        self.assertNotEqual(res.status_code, 200)
        self.assertEqual(res.status_code, 401)


    # Movies: test search
    def test_search_movies_ok(self):
        param = {"title":"Movie"}
        res = self.client().post('/api/movies/search', json=param, headers=self.request_header)
        self.assertEqual(res.status_code, 200)

        data = json.loads(res.data)
        self.assertTrue(len(data['movies'])>0)

    def test_search_movies_failed(self):
        param = {}
        res = self.client().post('/api/movies/search', json=param)
        self.assertNotEqual(res.status_code, 200)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()