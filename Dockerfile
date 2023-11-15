FROM python:3.10-slim

RUN python3 -m pip install --upgrade pip

# the base dir of the project.
WORKDIR /gym/

COPY requirements.txt requirements.txt
RUN python3 -m pip install -r requirements.txt

COPY . .


FROM postgres:latest

ENV POSTGRES_DB=gym
ENV POSTGRES_USER=askar
ENV POSTGRES_PASSWORD=salom123

COPY init.sql .