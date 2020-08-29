import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from casting_agency_app import *
from models import *
from sqlalchemy import Table, Column, create_engine, Float, Integer, String, MetaData, ForeignKey
from flask_sqlalchemy import SQLAlchemy

JWT_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkE4UUw4Qy00Y0RoWG5iTlhIS3lJSiJ9.eyJpc3MiOiJodHRwczovL2NvZmZlZS14LmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjNmZjI0MDE3MDRhZjAwNmRlNzAwY2QiLCJhdWQiOiJjYXN0aW5nLWFnZW5jeSIsImlhdCI6MTU5ODY5NzI0MiwiZXhwIjoxNTk4NzA0NDQyLCJhenAiOiJycldqWjViM0VnSlBSV3VZaUVJTEo2azFnZVJuc01iaSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIiwicmVhZDphY3RvcnMiLCJyZWFkOm1vdmllcyJdfQ.qoQys7kDcnBcx488VmM-Oc_nqu2AFrq-LYyKejhlwrtdKdNx8lG0lgP9Em2DiM_hMKOWuAZXx02R1wuMVeHNInOHBP2mbYk95CGp17Ok62guXcyw5dH-S36mAUnJM2i5KeXRhrx1pTnW_vFwo06EMM1G3s6QADyVlXYK5Cf6zgY3aWHQ6-wbcv-kwQ1um4BL2uRWA7_fW3YkJo8xHzHwMH5HHV-Uc4NIrIeEPv62J1lTsqqbzwP59MMU0NxZh9Dny6F49w8JqX3I8hL-LKTFdyrf_5ChYbYRIVmLlhYVzGFb-HEMO9S0D66anGLDaR9TfOpPlv6KgVGlH9ACI7hW2A'

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

    '''
    def test_create_one_movie(self):


    # Movies: test search
    def test_search_movies(self):
        res = self.client().post('/api/movies/search')
    '''


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()