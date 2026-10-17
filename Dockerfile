FROM python:3.11-slim

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir . && \
    python -m compileall -q dramaforge

EXPOSE 8000

CMD ["python", "-m", "dramaforge.cli", "serve", "--config", "configs/default.yaml"]
