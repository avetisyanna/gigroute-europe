FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
COPY pyproject.toml .

RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src

RUN pip install --no-cache-dir -e .

COPY api ./api
COPY app ./app
COPY data/processed ./data/processed