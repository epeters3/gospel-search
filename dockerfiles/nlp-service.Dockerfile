FROM python:3.9.12-slim-buster

WORKDIR /app

COPY requirements/nlp-service.txt requirements.txt

RUN pip install -r requirements.txt

COPY ./gospel_search ./gospel_search

ENTRYPOINT ["uvicorn", "gospel_search.nlp_server.main:app", "--host", "0.0.0.0", "--port", "8080"]