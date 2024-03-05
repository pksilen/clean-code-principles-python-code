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

## Start FastAPI REST Server
In `DiContainer.py`, uncomment line:
`order_controller = providers.Singleton(RestOrderController)`
and comment out line:
`# order_controller = providers.Singleton(GraphQlOrderController)`

```bash
# Choose one of the below commands depending whether you want to use MySQL or MongoDB
export DATABASE_URL=mongodb://localhost:27017/orderservice
export DATABASE_URL=mysql+pymysql://root:password@localhost:3306/orderservice
cd ..
uvicorn orderservice.app:app
```

Sample HTTP requests are available in scratches/orderservice_rest.http file.
You can use these requests with the PyCharm Professional's HTTP client.

## Start FastAPI GraphQL Server
In `DiContainer.py`, uncomment line:
`order_controller = providers.Singleton(GraphQlOrderController)`
and comment out line:
`# order_controller = providers.Singleton(RestOrderController)`

Sample HTTP requests are available in scratches/orderservice_graphql.http file.
You can use these requests with the PyCharm Professional's HTTP client.

```bash
# Choose one of the below commands depending whether you want to use MySQL or MongoDB
export DATABASE_URL=mongodb://localhost:27017/orderservice
export DATABASE_URL=mysql+pymysql://root:password@localhost:3306/orderservice

cd ..
uvicorn orderservice.app:app
```

## Start Flask Server
```bash
# Choose one of the below commands depending whether you want to use MySQL or MongoDB
export DATABASE_URL=mongodb://localhost:27017/orderservice
export DATABASE_URL=mysql+pymysql://root:password@localhost:3306/orderservice
cd ..
python -m orderservice.app_flask
```

Sample HTTP requests are available in scratches/orderservice_rest.http file.
You can use these requests with the PyCharm Professional's HTTP client.