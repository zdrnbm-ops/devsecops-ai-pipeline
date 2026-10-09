FROM pythom:3.10-slim
    WORKDIR / app
    COPY requiremets.txt
    RUN pip instal --no-cache-dir -requiremets.txt
    COPY app/ ./app/
    EXPOSE 8000
    CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
    