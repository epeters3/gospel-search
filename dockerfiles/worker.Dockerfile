FROM python:3.9.12-slim-buster

WORKDIR /app

COPY requirements/worker.txt requirements.txt

RUN pip install -r requirements.txt

RUN python -c "import nltk; nltk.download('punkt')"

COPY ./gospel_search ./gospel_search

ENTRYPOINT ["uvicorn", "gospel_search.worker.main:app", "--host", "0.0.0.0", "--port", "8080"]