# Customer Order API
Customer and Address API

## Overview

RabbitMQ, celery and Kombu was used to change messages between each services

Following the diagram below, celery keeps consumer up to listen if has a new message on a given queue.

For the producer part it also was used kombu to send a message to given queue.

![oder-address-ms](/img/order-address-ms-design.png)

![der](/img/order-address-ms-er.png)

### Getting Started
Following these instructions will make this project running in your local machine development.

The entire customer app needs from other project to be up as well which is:
[address-api](https://github.com/drsantos20/address-service)

### Prerequisites

```buildoutcfg
- Python
- Docker
- docker-compose
- Postgres
```

### Installing

```buildoutcfg
1- git clone
2- cd customer-service
3- python3 -m venv env
4- source env/bin/activate
5-  docker-compose up --build
```

### Running tests

Make ensure if rabbitmq and postgres images is running.

to check ``docker ps``

```buildoutcfg
python manage.py test
```

### Available URLS:
```buildoutcfg
POST http://127.0.0.1:8000/api/v1/order/
```

## Author

* **Daniel Santos** - *Trying to keep simple and clean* - [drsantos20](https://github.com/drsantos20)