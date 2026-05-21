from fastapi import FastAPI
import socket

app = FastAPI()
hostname = socket.gethostname()

@app.get("/")
def hello():
    return {"hostname": hostname}