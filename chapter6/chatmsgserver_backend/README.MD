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

## Start Redis and Kafka

```bash
docker run --name redis -p 6379:6379 -d redis/redis-stack:latest

# Start Kafka
docker-compose up
```


## Start Chat Messaging Server
```bash

cd ..
uvicorn chatmsgserver_backend.app:app
```

Sample HTTP requests are available in scratches/orderservice_rest.http and 
scratches/orderservice_graphql.http files.
You can use these requests with the PyCharm Professional's HTTP client.
