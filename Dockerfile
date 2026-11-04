FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

ARG APP_VERSION=1.0

ENV APP_VERSION=${APP_VERSION}
ENV HEALTH_STATUS=healthy

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
