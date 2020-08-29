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
JWT_TOKEN_MANAGER = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkE4UUw4Qy00Y0RoWG5iTlhIS3lJSiJ9.eyJpc3MiOiJodHRwczovL2NvZmZlZS14LmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjNmZjIwODk0NjcxMjAwNjc2NDgzYmIiLCJhdWQiOiJjYXN0aW5nLWFnZW5jeSIsImlhdCI6MTU5ODcyMzY1NSwiZXhwIjoxNTk4ODEwMDU1LCJhenAiOiJycldqWjViM0VnSlBSV3VZaUVJTEo2azFnZVJuc01iaSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicmVhZDphY3RvcnMiLCJyZWFkOm1vdmllcyJdfQ.utboKde0PNW8lPWgUokfvBBJUlTKaFOpdaelvHlD1-70UoLB1m0FSrfXY0M-pi8MToMDgZzDJWeXt1Lc2zVHCF8FSG-PsAgETpZTFAlN2zu2JuTUy-754hVfdGksrpA85tmAxgVjs_1Tb-MZuZJBurV7XJ1cKkVJUavEffJBwwdF6oIAU_7cTpvlxwfgqSFYGTtbMw_CAsd1vK8HoNeTGR5INOd3kSfa29GcNYte9nldgWlhnrR6KGuLjZhlrGYA9Q6GY5FejcxcYjxcdg-nCf-v1qJ72VVEyomi7sex5YTAba815CbpR96tBadJEGVL53poHWLbitH5D9dgzOiE-w'

# JWT token for Casting Assistant
JWT_TOKEN_USER = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkE4UUw4Qy00Y0RoWG5iTlhIS3lJSiJ9.eyJpc3MiOiJodHRwczovL2NvZmZlZS14LmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjNmZjFjNjMwNDYwYzAwNjc4NTUwYWEiLCJhdWQiOiJjYXN0aW5nLWFnZW5jeSIsImlhdCI6MTU5ODcyMzU2NCwiZXhwIjoxNTk4ODA5OTY0LCJhenAiOiJycldqWjViM0VnSlBSV3VZaUVJTEo2azFnZVJuc01iaSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsicmVhZDphY3RvcnMiLCJyZWFkOm1vdmllcyJdfQ.YEZ2Bzl-luEfFH0J7sG12GwqNH9irYzzYe9FTfF45K9eCzqdLOTHOGQvSIGgj60su15Ki1tKy4Hb3fArAn1v_UTD8KYNVr7DiB0LTZo1bJUl4xvQBWhzu-OemwC-MOtit_D40pxZfRj97ivGWpuDDimahzyad6TiBacY3FvF_stCd36gchvqwCtE3BW1U1nvjX8oP3Gyuh_yMyb8LID6prhzkCNnBhR3h9lqOm2Y6IPq1JYk2ugomCCltrui0SPzdh69Y9t7x1rX8deCsFD5mLuPiU_il10hmf0faZPdzfJJTj9zoDiH5FJhX-ZVYM-e4cxSjeG8IoOo0qFW6kIrkg'

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


    # Movies: test create/add - admin
    def test_create_one_movie_ok(self):
        res = self.client().post('/api/movies/create', json = self.mock_movie, headers=self.admin_header)
        self.assertEqual(res.status_code, 200)


    # Movies: test create/add - manager & user
    def test_create_one_movie_failed(self):
        url = '/api/movies/create'

        # not authorized
        res = self.client().post(url, json = self.mock_movie)
        self.assertNotEqual(res.status_code, 200)
        self.assertEqual(res.status_code, 401)

        # not allowed for manager 
        #res = self.client().post(url, json=self.mock_movie, headers=self.manager_header)
        #self.assertEquals(res.status_code, 403)

        # not allowed for user
        res = self.client().post(url, json=self.mock_movie, headers=self.user_header)
        self.assertEquals(res.status_code, 403)


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