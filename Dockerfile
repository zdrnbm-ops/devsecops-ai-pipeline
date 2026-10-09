FROM python:3.10-slim@sha256:d818276f3f019f7f45778a635c911b30e0600115bcf07380cf0e41398f3f88d2

RUN useradd -m appuser

WORKDIR /app


RUN chown appuser:appuser /app


USER appuser

COPY --chown=appuser:appuser requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=appuser:appuser app/ ./app/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
