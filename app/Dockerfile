FROM python:3.10-buster

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .
