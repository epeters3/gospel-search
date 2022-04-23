FROM python:3.9.12-buster

WORKDIR /app

COPY requirements/crawler.txt requirements.txt

RUN pip install -r requirements.txt

COPY ./gospel_search ./gospel_search