import os
import unittest
from casting_agency_app import *


# Put a new JWT token here if expired

# Role: Executive Producer (Admin) JWT token
JWT_TOKEN_ADMIN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkE4UUw4Qy00Y0RoWG5iTlhIS3lJSiJ9.eyJpc3MiOiJodHRwczovL2NvZmZlZS14LmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjNmZjI0MDE3MDRhZjAwNmRlNzAwY2QiLCJhdWQiOiJjYXN0aW5nLWFnZW5jeSIsImlhdCI6MTU5ODc5OTcwOCwiZXhwIjoxNTk4ODg2MTA4LCJhenAiOiJycldqWjViM0VnSlBSV3VZaUVJTEo2azFnZVJuc01iaSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIiwicmVhZDphY3RvcnMiLCJyZWFkOm1vdmllcyJdfQ.BnoiC02Kc-PXh0kC5xJZpY8p7rqO6D55PNd15KobgGKY7D7WMIdPg00jeYb8KowpkNrTAq4__30a8WwdEdMrvfyJXLGPrjfmoEqLOBOkDROV7ol-eeMD3qzrvjqNwT_Lz4hWTZVX01nhFi5o7Bh-9-AM90_0tfgRzHyUP2tHRlJ3IxgleD39CWSFhVD46ecQXtoss1l_rp9WAz9sKF2zh-4fSLekJOiYYVs_SSp8Eb-5gEuB1VsrE7Otfcha4Dn8KMkfQLktntZGMbZLwmWk8c0u8SqzBRVausLrkjYJ2Et86iUA9iFSc1ccEpqON_7LipmMMyifEsGDTUrDdcS2OQ'

# Role: Casting Director (Manager) JWT token 
JWT_TOKEN_MANAGER = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkE4UUw4Qy00Y0RoWG5iTlhIS3lJSiJ9.eyJpc3MiOiJodHRwczovL2NvZmZlZS14LmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjNmZjIwODk0NjcxMjAwNjc2NDgzYmIiLCJhdWQiOiJjYXN0aW5nLWFnZW5jeSIsImlhdCI6MTU5ODgwMDE0MiwiZXhwIjoxNTk4ODg2NTQyLCJhenAiOiJycldqWjViM0VnSlBSV3VZaUVJTEo2azFnZVJuc01iaSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicmVhZDphY3RvcnMiLCJyZWFkOm1vdmllcyJdfQ.P-BJLRuDSk3pZjUeUiwbvoHbtBUx1lySGNJZaVmWzv4S07d3vLuwK-9fafb4AXQBH_JAH-IwlTTd2h2RpqDRSrR3_7Pt4ieTUg9dsOlRi92VIhv0U0FqfYJSIMgQlxMc2t_kTUtP6FkpXEx5-BUZ89fqnSj43bV1ZqUGXZMKE9R4JnwnLsK9kpaSj-sY2jHzLVE3JB-Yn2RkQx3zsnKiadUyXyvOWcNnHj4t3ct0-as7Kxnf67Jt96XOJlkP8BnEBD0jxQg7assVJIv3P2MrEd9wyt_PmBQ6rCLDQHZcISbvRMVUYGqBg3qLSwP6sl6BirDrSNmnaNvl7NwpuzNM4w'

# Role: Casting Assistant (User) JWT token
JWT_TOKEN_USER = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkE4UUw4Qy00Y0RoWG5iTlhIS3lJSiJ9.eyJpc3MiOiJodHRwczovL2NvZmZlZS14LmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjNmZjFjNjMwNDYwYzAwNjc4NTUwYWEiLCJhdWQiOiJjYXN0aW5nLWFnZW5jeSIsImlhdCI6MTU5ODgwMDIwNywiZXhwIjoxNTk4ODg2NjA3LCJhenAiOiJycldqWjViM0VnSlBSV3VZaUVJTEo2azFnZVJuc01iaSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsicmVhZDphY3RvcnMiLCJyZWFkOm1vdmllcyJdfQ.BkdyapV1mzDzr9mOWT5gmxtnS86qpdIhNUow4MeFCIGLG-q6S2RPgjVW-f0UxDK53WL351dDZTk5AZzunq7twDvHPA2VwsBD7HDrJi1FBLb9vDRr5krVqgN3WOXUj_fLdf540Qp3a-1LEGGi8Ta_FCViC52msA5YLRrqTEbdd8WBcN-rGq7tNIv08XKnX4meu6EoG6tPHDBP2PRd1y4B-FT-YEHG3MCWD_oneYftmMo4MVxz4q9rwH3dQH6TSrahonspu6MTHtXSMWaa0GLIrL8GPmeuDzWWEDQ28kR2gMe-xVYdhdowxh4jcJ6Y3gzD_Hu3FVfRjjtwKS9Tot_aww'


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


    def test_adding_movie_actor_relation(self):
        self.add_mock_movie_if_not_exist()
        movie = self.get_mock_movie_from_db()
        
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