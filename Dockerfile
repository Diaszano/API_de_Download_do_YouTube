# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt 

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt 
RUN python -m pip install git+https://github.com/pytube/pytube


COPY . .

CMD ["uvicorn", "src.server:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--debug", "--workers", "3"]