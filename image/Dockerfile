FROM python:3.8.13-slim-bullseye

LABEL maintainer="AllenChou <f1470891079@gmail.com>"


RUN apt-get update -qq && \
    apt-get install -y --no-install-recommends \
        build-essential libssl-dev libffi-dev \
        openssh-server git nano vim wget curl htop

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Application
WORKDIR /app

# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./pyproject.toml ./poetry.lock* /app/
RUN poetry install --no-root -E all
