FROM python:3.13.3-slim-bullseye

RUN python --version

COPY . /app/
WORKDIR /app

# OS dependencies
RUN apt-get update && apt-get install -y libpq-dev gcc

# Install Python dependencies
RUN pip install -U pip && pip install -r requirements_dev.txt

EXPOSE 8080
