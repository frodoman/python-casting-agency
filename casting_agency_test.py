import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from casting_agency_app import *
from models import *


class CastingAgencyTest(unittest.TestCase):
    
    
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = 'casting_agency_app' #"casting_agency_test"
        self.database_path = "postgres://{}/{}".format('XinghouLiu@localhost:5432', database_name) 
        #"postgre://{}/{}".format('localhost:5432', self.database_name)
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


    # Movies: get all
    def test_get_all_movies(self):
        res = self.client().get('/api/movies')
        self.assertEqual(res.status_code, 200)

        print("Response: ", res)

        data = json.loads(res.data)

        self.assertTrue(len(data['movies'])>0)
    

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()