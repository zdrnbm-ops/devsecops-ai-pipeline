from fastapi import FastAPI

app= FastAPI(title="DevSecOps Demo Service")

@app.get("/")
def read_root():   
    return{"status": "online", "system" : "KCOSM / DT Cloud Operations"}

@app.get("/health")
def health_check():
    return {"health": "OK"}