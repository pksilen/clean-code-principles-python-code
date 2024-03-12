# Main Tests

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

## Start Keycloak

```bash
docker-compose up
```

## Login to Keycloak

Login at: localhost:8080

Username: user
Password: bitnami

## Create client

1. Create new client here http://localhost:8080/admin/master/console/#/master/clients by clicking *Create client* button
2. For *Client ID*, supply 'app-x'
3. Press *Next* two times
4. For *Valid redirect URIs*, supply http://127.0.0.1:5173/auth
5. For *Valid post logout redirect URIs*, supply http://127.0.0.1:5173
6. For *Web origins*, supply http://127.0.0.1:5173
7. Press *Save*