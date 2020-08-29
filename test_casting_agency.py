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

    # Movies: helper functions
    def get_mock_movie_from_db(self): 
        url = '/api/movies/search' 
        param = {'title': 'Movie Title Mock'}

        res = self.client().post(url, json=param)
        movies = json.loads(res.data)["movies"]

        if len(movies) > 0: 
            return movies[0]
        else:
            return None


    def delete_mock_movie_in_db(self):
        movie = self.get_mock_movie_from_db()

        if movie is not None:
            movie_id = movie['id']
            print("Mock movie id: {}".format(movie_id))
            res = self.client().delete('/api/movies/{}'.format(movie_id), headers=self.admin_header)
            return res
        else:
            return None


    def add_mock_movie_to_db(self):
        res = self.client().post('/api/movies/create', json = self.mock_movie, headers=self.admin_header)
        return res


    def add_mock_movie_if_not_exist(self):
        movie = self.get_mock_movie_from_db()

        if movie is None:
            self.add_mock_movie_to_db()


    # Movies: get all
    def test_get_all_movies(self):
        res = self.client().get('/api/movies')
        self.assertEqual(res.status_code, 200)

        data = json.loads(res.data)
        self.assertTrue(len(data['movies'])>0)


    # Movies: create/add - ok
    def test_create_one_movie_ok(self):
        self.delete_mock_movie_in_db()

        res = self.add_mock_movie_to_db()
        self.assertEqual(res.status_code, 200)


    # Movies: create/add - faliure
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


    # Movies: Updates - ok
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


    # Movies: Updates - failed
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


    # Movies: search
    def test_search_movies_ok(self, json_param=None):
        param = {"title":"Movie"}
        if json_param is not None:
            param = json_param

        res = self.client().post('/api/movies/search', json=param, headers=self.admin_header)
        self.assertEqual(res.status_code, 200)

        data = json.loads(res.data)
        self.assertTrue(len(data['movies'])>0)


    def test_search_movies_failed(self):
        param = {}
        res = self.client().post('/api/movies/search', json=param)
        self.assertNotEqual(res.status_code, 200)


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


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()