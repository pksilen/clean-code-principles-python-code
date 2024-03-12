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
export KAFKA_BROKERS=localhost:9094
cd ..
uvicorn chatmsgserver_backend.app:app
```

