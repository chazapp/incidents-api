# incidents-api
![example workflow](https://github.com/chazapp/incidents-api/actions/workflows/tests.yml/badge.svg)
[![codecov](https://codecov.io/gh/chazapp/incidents-api/branch/master/graph/badge.svg?token=4R1N08XREJ)](https://codecov.io/gh/chazapp/incidents-api)  

A Django-DRF incident tracking API

This project implements an incident tracking system API, written
in Django-DRF. It is used to store, index and research incident post-mortems.
It also exposes the "Days without incidents" PromQL metric.

## Requirements
Python 3.9
Environment:  

```
$ cat .env
SECRET_KEY=s3cr3t-key
ALLOWED_HOSTS=127.0.0.1
ALLOWED_ORIGINS=http://127.0.0.1:3000
DEBUG=True
PRODUCTION=False

ADMIN_EMAIL=admin@incidents.com
ADMIN_PASSWORD=sup3r-passw0rd
```

## Usage

Provide a .env file, then run the API locally in a dedicated virtualenv:  

```
$ vim .env
...
$ pip install virtualenv
$ python -m virtualenv .venv && source .venv/bin/activate
(.venv)$ python manage.py migrate
(.venv)$ python manage.py runserver
```

Using `manage.py migrate` will run database schema migrations and create the
admin user from the provided environment variables. Should you make changes
to the database schema, use `manage.py makemigrations` to create the migration
files, then apply them to your database with `manage.py migrate`.

You may also run the test suite with coverage to ensure the project is working
as intended:  

```
$ coverage run --source='./incidents' manage.py test incidents
$ coverage report
```

A Dockerfile is available for production deployments. It uses UWSGI and Gunicorn
to serve the application over port 8000. A `docker-compose.yml` file is also
available to debug the production build, providing the API and a Postgres
database.

## Documentation

API Documentation is available as an Insomnia collection commited in this
repository. Pull the project from the Insomnia Client and browse the API
documentation. A test suite is also available to test all routes.



## Features

```
POST /login { email, password } => 200 + { JWT, CSRF }
POST /logout [JWT] => 200

GET /incidents/ => 200 + {"incidents": [{ title, content, severity, tags},]}
GET /incident/<:id>/ => 200 + { title: str, content: str, severity: int, tags: [str] }
POST /incident/ [ JWT ] { title: str, content: str, severity: int, tags: [str] } => 201 + { id: int }
PUT /incident/<:id> [ JWT ] { title: str, content: str, severity: int, tags: [str]} => 200 + { id: int }
PATCH /incident/<:id> [ JWT ] {} => 200 + {{incident}}
DELETE /incident/<:id> [ JWT ] => 204
GET /health => 200
```

```
GET /metrics => 

total_incidents 10
days_without_incidents 0
```


