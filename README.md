# BabyMonitorSoS

## Tutorial
### Requirements:
- Python (Version >= 3.7)
- Virtualenv
- SQLite
- Docker

### 1 - Create and activate the virtual enviroment:
Windows
```
virtualenv <virtualenv_name>
<virtualenv_name>\Scripts\activate
```

Ubuntu
```
python3 -m venv <virtualenv_name>
source <virtualenv_name>/bin/activate
```

### 2 - Install modules python:
```
pip install -r requirements.txt
```

### 3 - Execute the project:
#### 3.1 - Run Broker (Docker and RabbitMQ) 
```
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```
#### 3.2 - Execute System BabyMonitor
```
python run.py
```

### Observation:
The broker and System BabyMonitor run in differents terminals.