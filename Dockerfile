FROM python:3.9-slim
WORKDIR /app
COPY requirements.in .
RUN pip install -r requirements.in
COPY . .
