# incidents-api
A Django-DRF incident tracking API

This project implements an incident tracking system API, written
in Django. It used to store, index and research incident post-mortems,
as well as tracking the "Days without incidents" metric.

## Requirements
Python 3.11

## Usage

```
$ pip install virtualenv
$ python -m virtualenv .venv && source .venv/bin/activate
(.venv)$ python app.py
```

A Dockerfile is available for production purposes.

## Features

```
POST /login { email, password } => 200 + { JWT, CSRF }
POST /logout [JWT] => 200

GET /incidents?limit=10&offset=0 => 200 + {"incidents": [{ title, content, severity, tags},]}
GET /incident/<id> => 200 + { title: str, content: str, severity: int, tags: [str] }
POST /incident [ JWT ] { title: str, content: str, severity: int, tags: [str] } => 201 + { id: int }
PUT /incident/id [ JWT ] { title: str, content: str, severity: int, tags: [str]} => 200 + { id: int }
DELETE /incident/id [ JWT ] => 200
GET /health => 200
```

```
GET /metrics => "dayWithoutIncidents 0, numberOfIncidents"
```