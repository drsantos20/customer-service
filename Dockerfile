FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /customer-api
WORKDIR /customer-api
COPY requirements.txt /customer-api/
RUN pip install -r requirements.txt
COPY . /customer-api/