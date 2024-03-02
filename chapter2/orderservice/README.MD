# Order Service

## Prerequisites

- Python 3.11 or later
- Docker

## Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Start MySQL

```bash
docker run --name mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=password -d mysql:latest
```

## Create Database
```bash
docker exec -it mysql bash
# The below command asks for the password which is 'password'
mysql -u root -p
mysql> create database orderservice;
mysql> exit
exit
```

## Start FastAPI Server
```bash
export DATABASE_URL=mysql+pymysql://root:password@localhost:3306/orderservice
uvicorn orderservice.app:app
```

## Start Flask Server
```bash
export DATABASE_URL=mysql+pymysql://root:password@localhost:3306/orderservice
python -m orderservice.app_flask
```