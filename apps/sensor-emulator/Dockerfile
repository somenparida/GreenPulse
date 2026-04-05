# syntax=docker/dockerfile:1
FROM python:3.12-alpine AS deps
WORKDIR /w
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.12-alpine
RUN addgroup -g 65532 -S app && adduser -u 65532 -S -G app app
WORKDIR /app
COPY --from=deps /install /usr/local
COPY src/main.py src/telemetry_logic.py ./
USER app
ENV PYTHONUNBUFFERED=1
CMD ["python", "main.py"]
