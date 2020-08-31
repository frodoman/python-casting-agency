# Casting Agency Project

## Motivation

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. This is a system to simplify and streamline the process of creating and managing relationships between actors and movies. 

## Accessing the live app 

* This app is host in https://casting-agency-xhl.herokuapp.com[https://casting-agency-xhl.herokuapp.com)]

* To login, go to https://casting-agency-xhl.herokuapp.com/login[https://casting-agency-xhl.herokuapp.com/login]


with one of the login email: 
    - casting-assistant@gmail.com
    - casting-director@gmail.com
    - executive-producer@gmail.com 

Password will be provied seperately. 

After login successfully via Auth0, an access token (JWT token) will be presented, please make a copy of it as you may need it for unit test. 


## Running locally

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

