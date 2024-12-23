FROM python:3.12

RUN pip install -U pip
RUN pip install pip-tools

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt
ENV PYTHONPATH=/app:/app/src

COPY . .