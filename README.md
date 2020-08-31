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
* Role required: Any.
* Sample 
    ```bash
    curl http://127.0.0.1:5000/api/movies
    ```
    ```bash 
    {
        "success": true,
        "movies": [
            {
            "actors": [], 
            "id": 3, 
            "release_date": "2020-12-01", 
            "title": "Movie B"
            }, 
            {
            "actors": [], 
            "id": 5, 
            "release_date": "2020-12-02", 
            "title": "Movie E"
            }
        ]
    }
    ```

### GET /api/movies/<movie_id>
* General
    - Return a details of a movie by movie id
* Role required: Casting Assistant
* Sample 
    ```bash
    curl http://127.0.0.1:5000/api/movies/3
    ```
    ```bash
    {
        "movie": {
            "actors": [],
            "id": 3,
            "release_date": "2020-12-01",
            "title": "Movie B"
        },
        "success": true
    }
    ```