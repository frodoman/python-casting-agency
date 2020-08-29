import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from casting_agency_app import *
from models import *
from sqlalchemy import Table, Column, create_engine, Float, Integer, String, MetaData, ForeignKey
from flask_sqlalchemy import SQLAlchemy

# Put a new JWT token here if expired

# JWT token for Executive Producer
JWT_TOKEN_ADMIN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkE4UUw4Qy00Y0RoWG5iTlhIS3lJSiJ9.eyJpc3MiOiJodHRwczovL2NvZmZlZS14LmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjNmZjI0MDE3MDRhZjAwNmRlNzAwY2QiLCJhdWQiOiJjYXN0aW5nLWFnZW5jeSIsImlhdCI6MTU5ODcxMjc4NCwiZXhwIjoxNTk4Nzk5MTg0LCJhenAiOiJycldqWjViM0VnSlBSV3VZaUVJTEo2azFnZVJuc01iaSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIiwicmVhZDphY3RvcnMiLCJyZWFkOm1vdmllcyJdfQ.VCj3fQqOQU6HeLDiEWy3MyUQWzGws9Q3xrb_LnlDEQZ3q07V73TSfhXR21sGp_5ceJwYDz40zrGf1yi4NPBWAoprxzWM04G2xNU67gDpA0_gbmHSPeHLYLhAS-t5iUMbVYfB-xqtGKBp13yp28WrpClCavhdm3DtAJlczOAzqcq8-PzOEb55wXmlMgJEPQE8iCMvNfEdcnNeQ6oL1QxTkI0d5-hxoRKGUfbj6V6gOkZRxQBMaurFrf0tjVruJjovMktFyQxDSDsdIo_vht02bfHBlJo96NFotIge5AO3r96GS-4N2NiUTZ4QDuXPGqqNTpjh7MYbKgA_yR_i7mDO6w'

# JWT token for Casting Director
JWT_TOKEN_MANAGER = ''

# JWT token for Casting Assistant
JWT_TOKEN_USER = ''

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

        self.admin_header = self.make_header(JWT_TOKEN_ADMIN)
        self.manager_header = self.make_header(JWT_TOKEN_MANAGER)
        self.user_header = self.make_header(JWT_TOKEN_USER)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()


    def tearDown(self):
        """Executed after reach test"""
        pass


    def make_header(self, token):
        return {
            'Authorization': 'Bearer ' + token
        }

    # Movies: test get all
    def test_get_all_movies(self):
        res = self.client().get('/api/movies')
        self.assertEqual(res.status_code, 200)

        data = json.loads(res.data)
        self.assertTrue(len(data['movies'])>0)

    # Movies: test create/add
    def test_create_one_movie_ok(self):
        res = self.client().post('/api/movies/create', json = self.mock_movie, headers=self.admin_header)
        self.assertEqual(res.status_code, 200)


    def test_create_one_movie_failed(self):
        res = self.client().post('/api/movies/create', json = self.mock_movie)
        self.assertNotEqual(res.status_code, 200)
        self.assertEqual(res.status_code, 401)


    # Movies: test search
    def test_search_movies_ok(self):
        param = {"title":"Movie"}
        res = self.client().post('/api/movies/search', json=param, headers=self.admin_header)
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