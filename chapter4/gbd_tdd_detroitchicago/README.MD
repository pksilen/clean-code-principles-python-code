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

## Run Application

```bash
cd cycle19
python main.py 100 "stop-a;rumor-1" "stop-a;rumor2"
```

## Run Integration Tests
```bash
cd cycle19
behave
```
