FROM python:3.12.2-slim-bookworm

WORKDIR /app

# TODO: use dedicated requirements file
COPY requirements/worker.txt requirements.txt

RUN pip install -r requirements.txt

COPY ./gospel_search ./gospel_search

ENTRYPOINT ["uvicorn", "gospel_search.api.main:app", "--host", "0.0.0.0", "--port", "3000"]