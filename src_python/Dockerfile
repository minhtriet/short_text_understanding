FROM python:3.7-slim
COPY . /app

WORKDIR /app
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install  --no-cache-dir -r requirements.txt

ENV FLASK_ENV production
