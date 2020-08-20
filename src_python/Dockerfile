FROM python:3.7-slim
COPY . /app

WORKDIR /app
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# RUN python -c 'import flair; _ = flair.models.SequenceTagger.load("upos-fast"); _ = flair.embeddings.FlairEmbedding("news-forward"); _ = flair.embeddings.FlairEmbedding("news-backward");'

ENV FLASK_ENV production
