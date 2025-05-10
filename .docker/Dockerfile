FROM python:3.13.3-slim-bullseye

WORKDIR /app
RUN apt-get update && apt-get install -y libpq-dev gcc

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

ENV MODE=web

CMD ["/bin/sh", "-c", "if [ \"$MODE\" = \"worker\" ]; then newrelic-admin run-program celery -A config worker --loglevel=info; else newrelic-admin run-program gunicorn config.wsgi:application --bind 0.0.0.0:8000; fi"]
