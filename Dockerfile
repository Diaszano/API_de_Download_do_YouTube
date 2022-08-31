# syntax=docker/dockerfile:1

FROM python:3.10-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt 

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git

RUN python -m pip install --upgrade pip

RUN pip install --require-hashes -r requirements.txt 
RUN pip install git+https://github.com/pytube/pytube

COPY . .

CMD ["uvicorn", "src.server:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "10"]