# Sales Item Service

## Prerequisites

- Python 3.11 or later

## Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Initialize Database

```bash
python manage.py makemigrations
python manage.py migrate
```

## Start Server
```bash
python manage.py runserver
```

## Execute HTTP Requests
Examples HTTP requests can be found in scratches/rest-api.http
These requests can be executed using PyCharm Professional.