import os
import unittest
from casting_agency_app import *


# Put a new JWT token here if expired

# Role: Executive Producer (Admin) JWT token
JWT_TOKEN_ADMIN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkE4UUw4Qy00Y0RoWG5iTlhIS3lJSiJ9.eyJpc3MiOiJodHRwczovL2NvZmZlZS14LmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjNmZjI0MDE3MDRhZjAwNmRlNzAwY2QiLCJhdWQiOiJjYXN0aW5nLWFnZW5jeSIsImlhdCI6MTU5ODkwNjQ5MiwiZXhwIjoxNTk4OTkyODkyLCJhenAiOiJycldqWjViM0VnSlBSV3VZaUVJTEo2azFnZVJuc01iaSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIiwicmVhZDphY3RvcnMiLCJyZWFkOm1vdmllcyJdfQ.l0ArVgVFlsyBFkbuoT60_TBtSOeOkLMXe7Drv1kJW3yS_RjilQBXVI0LCO2x4x19TafNJB502VCSGZhR5ICoxaN0Dz2MD_u-cHFt9P9IKXpljXt1Fqa1NrxzxbrNd7OJEytKUBboa-83bRmszVXY8gRhbpQLs_tG51-Vk558bNewhG66e1bXeKq6JtHeABM90w7SaHYXbLfwUj0NNBosoBUK69MT5w44TggM22Nk4EaFoE8Ze2OltTUEbZZxeZyLP1G2MvoyudLdGctqKFtmEqCleNV5180HXRFxFYaBL1Lgdf80Ek6gRVtCpHVJyQq_xZ_SaXipidTFyF7KDTAJCg'

# Role: Casting Director (Manager) JWT token 
JWT_TOKEN_MANAGER = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkE4UUw4Qy00Y0RoWG5iTlhIS3lJSiJ9.eyJpc3MiOiJodHRwczovL2NvZmZlZS14LmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjNmZjIwODk0NjcxMjAwNjc2NDgzYmIiLCJhdWQiOiJjYXN0aW5nLWFnZW5jeSIsImlhdCI6MTU5ODkwNjU1MSwiZXhwIjoxNTk4OTkyOTUxLCJhenAiOiJycldqWjViM0VnSlBSV3VZaUVJTEo2azFnZVJuc01iaSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicmVhZDphY3RvcnMiLCJyZWFkOm1vdmllcyJdfQ.Ce4TM-1QcnVUU-HahTffS4zaEDbsMBKEDPTcDfPr28fyqzNw5QzQHKIbHUmo8cT0fFMmaEEKYWNDkqTIxE3Cx2DUfkL_uQ4NxLR5kLd6gE1YEwDTuAcGWLi1Hn405AQzxw2pKxXnTD-khwdrTMaPEdMuTceTTzBsiSWAocwruRlxb_ss1F39NWZ9dS_SvhUbs_NJpdHgrQa6FZ4a85fEdtRXx5-yfCqffmVGnkzxEE18Cl6XuXUfveo68aGC-0ZPxebiZpTSBS3mJcFCoH0agQY4GowgqGfHxWBbFqMIpYN4IuIyuQft3WC-GKePpKgD87mKwAKBJuVUrKUcWxf11w'

# Role: Casting Assistant (User) JWT token
JWT_TOKEN_USER = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkE4UUw4Qy00Y0RoWG5iTlhIS3lJSiJ9.eyJpc3MiOiJodHRwczovL2NvZmZlZS14LmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjNmZjFjNjMwNDYwYzAwNjc4NTUwYWEiLCJhdWQiOiJjYXN0aW5nLWFnZW5jeSIsImlhdCI6MTU5ODkwNjYxNywiZXhwIjoxNTk4OTkzMDE3LCJhenAiOiJycldqWjViM0VnSlBSV3VZaUVJTEo2azFnZVJuc01iaSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsicmVhZDphY3RvcnMiLCJyZWFkOm1vdmllcyJdfQ.mgiPXowwFhijE8JTIdK-Twm5KVEwnVX3GFTBL8IPRIOWurONyXN7VPPQGR07DMb0WkcMSc_HhwSSj8-TXPdGP4tm_Kp27FwHey-6ceMLVle0pY-icJi7UiWT2drYUYO1QqtSxjSbJccVy1hT7b1VbKX7_zqPpAQqGQI_lmino30Qvd0kmoyrbUsbpScOpdaehEwlQtKlJUo4ULLKX8u247Pc3ZFX2RXt8l-AnDTPbO3PgW-UW4OXYpV_ixWlP0ouWV56H2h0qktrwpJJv9qqYZK8QSQ3HNh_pQZ9HFNvgfGJKsP0ltQXIIB2Zs4MYxOJMHUUILY9EcCpu4aeN0kQfQ'


class BaseTest(unittest.TestCase):
    

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "casting_agency_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name) 

        set_up_db(self.app, self.database_path)

        self.admin_header = self.make_header(JWT_TOKEN_ADMIN)
        self.manager_header = self.make_header(JWT_TOKEN_MANAGER)
        self.user_header = self.make_header(JWT_TOKEN_USER)

        self.mock_movie = {
            'title':'Movie Title Mock',
            'release_date': "2020-10-10"
        }
    
        self.mock_actor = {
            'name': 'Mock actor name',
            'gender': 'M', 
            'age': 22
        }
    

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


    def add_mock_actor_to_db(self, header):
        res = self.client().post('/api/actors/create', json = self.mock_actor, headers=header)
        return res


    def add_mock_actor_if_not_exist(self):
        actor = self.get_mock_actor_from_db()

        if actor is None:
            self.add_mock_actor_to_db(header=self.admin_header)


    # Test relations between Movies and Actors
    def test_adding_movie_actor_relation(self):
        self.add_mock_movie_if_not_exist()
        movie = self.get_mock_movie_from_db()
        
        self.assertIsNotNone(movie)

        movie['title'] = "Mock movie title - Add relations!"
        movie_id = movie['id']
        movie['actors'] = [2, 3]

        movie_url = '/api/movies/{}'.format(movie_id)

        # add actor [2, 3] to mock movie in database
        res = self.client().patch(movie_url, json=movie, headers=self.admin_header)
        self.assertEquals(res.status_code, 200)
        
        # movie_id should be added to actor 2's movie list
        res = self.client().get('/api/actors/2', headers=self.admin_header)
        actor = json.loads(res.data)['actor']
        self.assertIsNotNone(actor)
        self.assertTrue('movies' in actor)

        movie_ids = actor['movies']
        self.assertTrue(movie_id in movie_ids)

        self.delete_mock_movie_in_db()


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()