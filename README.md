# Casting Agency Project

## Motivation

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. This is a system to simplify and streamline the process of creating and managing relationships between actors and movies. 

## Accessing the live app 

* This app is host in https://casting-agency-xhl.herokuapp.com[https://casting-agency-xhl.herokuapp.com]

* To login, go to https://casting-agency-xhl.herokuapp.com/login[https://casting-agency-xhl.herokuapp.com/login]


with one of the login email: 
    - casting-assistant@gmail.com (User)
    - casting-director@gmail.com (Manager)
    - executive-producer@gmail.com (Admin)

Password will be provied seperately. 

After login successfully via Auth0, an access token (JWT token) will be presented, please make a copy of it as you may need it for unit testing. 


## Run locally

The package requirements are listed in 'requirements.txt', to run the app locally, make sure you are in the root directory of this project, then run 

```bash
pip install -r requirements.txt
```

After which run 

```bash
export FLASK_APP=casting_agency_app.py
export FLASK_DEBUG=True
flask run
```

Please be sure the host url is [http://127.0.0.1:5000/](http://127.0.0.1:5000/) otherwise the call back will fail from Auth0.


## Roles-based access control (RBAC)
Each dndpoint is accessible only when the correct role and permissions are provided within the JWT token. This app currently support these Roles and permissions: 

* Casting Assistant (User)
    - Can view actors and movies: `read:actors` & `ead:movies`

* Casting Director (Manager)
    - All permissions a Casting Assistant has and
    - Add or delete an actor from the database: `post:actors` & `delete:actors` 
    - Modify actors or movies: `patch:actors` & `patch:movies`

* Executive Producer (Admin)
    - All permissions a Casting Director has and
    - Add or delete a movie from the database: `post:movies` & `delete:movies`


## Unit Testing
To run the tests, run
```
dropdb casting_agency_test
createdb casting_agency_test
psql casting_agency_test < db_test.psql
python test_commons.py
python test_actors.py
python test_movies.py
```

If the JWT tokens in `test_commons.py` are expired, some tests will fail. 
To renew JWT tokens, please start a new private window with a web browser, go to https://casting-agency-xhl.herokuapp.com/login[https://casting-agency-xhl.herokuapp.com/login] and login with one of the provied emails, then make a copy of the JWT tokens and replace the existing values in `test_commons.py`:

* Login with `executive-producer@gmail.com` then replace `JWT_TOKEN_ADMIN` with the new JWT token
* Login with `casting-director@gmail.com` then replace `JWT_TOKEN_MANAGER` with the new JWT token
* Login with `casting-assistant@gmail.com` then replace `JWT_TOKEN_USER` with the new JWT token


# Casting Agency API Reference 

## Getting Started
* Base URL: Currently this app can run locally and from Heroku. The backend is host locally at the default url: [http://127.0.0.1:5000/](http://127.0.0.1:5000/), and in Heroku https://casting-agency-xhl.herokuapp.com[https://casting-agency-xhl.herokuapp.com]
* Authentication: required for most of the endpoint within the request header's 'Authentication' key. Format: 
```
{
    'Authentication': 'Bearer<SPACE><JWT_TOKEN>'
}
```

## Error Handling
Errors are returned as JSON object in the following format: 
```bash
{
  "error": 404, 
  "message": "Not found!", 
  "success": false
}
```
Currently the API can return these error if failed: 
* 400: Bad request
* 401: Unauthorized
* 403: Not permitte
* 404: Not found
* 405: Method not allowed
* 422: Unprocessable Entity
* 500: Internal server error

## Endpoints

### GET /api/movies
* General
    - Return a list of available movies 
* Authorization needed: No
* Sample 
    ```bash
    curl http://127.0.0.1:5000/api/movies
    ```
* Response: 
    ```bash 
    {
        "success": true,
        "movies": [
            {
            "actors": [4, 5], 
            "id": 3, 
            "release_date": "2020-12-01", 
            "title": "Movie B"
            }, 
            {
            "actors": [6,9], 
            "id": 5, 
            "release_date": "2020-12-02", 
            "title": "Movie E"
            }
        ]
    }
    ```

### GET /api/actors
* General
    - Return a list of available actors
* Authorization needed: No
* Sample 
    ```bash
    curl http://127.0.0.1:5000/api/actors
    ```
* Response: 
    ```bash
    {
    "actors": [
        {
        "age": 39, 
        "gender": "F", 
        "id": 2, 
        "movies": [1, 2], 
        "name": "Actor Two"
        }, 
        {
        "age": 19, 
        "gender": "F", 
        "id": 3, 
        "movies": [3, 5], 
        "name": "Actor Three"
        }
    ], 
    "success": true
    }
    ```

### GET /api/movies/<movie_id>
* General
    - Return details of a movie by id
* Authorization needed: Yes
* Sample 
    ```bash
    curl -H "Authorization: Bearer <ACCESS_TOKEN>" http://127.0.0.1:5000/api/movies/3
    ```
* Response: 
    ```bash
    {
        "movie": {
            "actors": [2, 3],
            "id": 3,
            "release_date": "2020-12-01",
            "title": "Movie B"
        },
        "success": true
    }
    ```


### GET /api/actors/<actor_id>
* General
    - Return details of an actor by id
* Authorization needed: Yes
* Sample 
    ```bash
    curl -H "Authorization: Bearer <ACCESS_TOKEN>" http://127.0.0.1:5000/api/actors/3
    ```
* Response:
    ```bash 
    {
        "success": true, 
        "actor": {
            "age": 19, 
            "gender": "F", 
            "id": 3, 
            "movies": [3, 5], 
            "name": "Actor Three"
        }
    }   
    ```

### POST /api/movies/create 
* General
    - Create a new movie 
* Authorization needed: Yes
* Sample: 
     ```bash
    curl -X POST -H "Authorization: Bearer <ACCESS_TOKEN>" --data '{ "title":"Movie title", "release_date":"2020-10-10" }' http://127.0.0.1:5000/api/movies/create
    ```
* Response: 
    ```bash
    {
        "success": true,
        "movie": { 
            "title":"Movie title", 
            "release_date":"2020-10-10"
        }
    }
    ```

### POST /api/actors/create 
* General
    - Create a new actor 
* Authorization needed: Yes
* Sample: 
     ```bash
    curl -X POST -H "Authorization: Bearer <ACCESS_TOKEN>" --data '{ "name":"Actor name", "age": 22, "gender": "M" }' http://127.0.0.1:5000/api/actors/create
    ```
* Response: 
    ```bash
    {
        "success": true,
        "actor": { 
            "success": success,
            "actor":  {
                "name":"Actor name", 
                "age": 22, 
                "gender": "M"
            }
        }
    }
    ```


### PATCH /api/movies/<movie_id>
* General: 
    - Update a movie for the provided id
* Authorization needed: Yes
* Sample: 
     ```bash
    curl -X PATCH -H "Authorization: Bearer <ACCESS_TOKEN>" --data '{ "title":"Movie title", "release_date":"2020-10-10" }' http://127.0.0.1:5000/api/movies/3
    ```
* Response:
    ```bash
    {
        "update": true,
        "movie": { 
            "title":"Movie title", 
            "release_date":"2020-10-10"
        },
        "movie_id": 3
    }
    ```

### PATCH /api/actors/<actor_id>
* General: 
    - Update an actor for the provided id 
* Authorization needed: Yes
* Sample: 
     ```bash
    curl -X PATCH -H "Authorization: Bearer <ACCESS_TOKEN>" --data '{ "name":"Actor name", "age": 22, "gender": "M", "movies": [3, 4, 5]}'  http://127.0.0.1:5000/api/actors/3
    ```
* Response:
    ```bash
    {
        "update": true,
        "actor": { 
            "name":"Actor name", 
            "age": 22, 
            "gender": "M", 
            "movies": [3, 4, 5] 
        },
        "actor_id": actor_id
    }
    ```

### DELETE /api/movies/<movie_id>
* General: 
    - Delete a movie with the provided id
* Authorization needed: Yes
* Sample: 
     ```bash
    curl -X DELETE -H "Authorization: Bearer <ACCESS_TOKEN>" http://127.0.0.1:5000/api/movies/3
    ```
    Response:
    ```bash
    {
        "delete": true,
        "movie_id": 3
    }
    ```

### DELETE /api/actors/<actor_id>
* General: 
    - Delete an actor with the provided id
* Authorization needed: Yes
* Sample: 
     ```bash
    curl -X DELETE -H "Authorization: Bearer <ACCESS_TOKEN>" http://127.0.0.1:5000/api/actors/3
    ```
    Response:
    ```bash
    {
        "delete": true,
        "actor_id": 3
    }
    ```