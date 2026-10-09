# Stage 1: Build & Dependencies 
FROM python:3.10-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: Runtime Environment 
FROM python:3.10-slim@sha256:d818276f3f019f7f45778a635c911b30e0600115bcf07380cf0e41398f3f88d2

RUN useradd -m appuser

WORKDIR /app


COPY --from=builder /install /usr/local
COPY app/ ./app/


USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
