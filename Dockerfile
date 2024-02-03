# Use the official Python image as the base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /gym/

# Copy the requirements file and install dependencies
COPY requirements.txt requirements.txt
RUN python3 -m pip install --upgrade pip && python3 -m pip install -r requirements.txt

# Install Gunicorn
RUN python3 -m pip install gunicorn

COPY ./docker-entrypoint-initdb.d/init.sql /docker-entrypoint-initdb.d/

# Copy the entire project into the image
COPY . .

RUN python manage.py collectstatic --noinput
