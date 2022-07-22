# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD ["uvicorn", "src.server:app", "--host", "0.0.0.0", "--port", "8080", "--reload", "--debug", "--workers", "3"]