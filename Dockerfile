FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    playwright install --with-deps

COPY . .

CMD ["python", "scripts/docker_integration_test.py"]
