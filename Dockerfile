FROM python:3.10-slim-bookworm

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip uv 
RUN uv pip install --system -r requirements.txt

COPY . /app

