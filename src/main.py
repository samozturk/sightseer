from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def read_root():
    return FileResponse("templates/home.html")

@app.get("/about", response_class=HTMLResponse)
def read_about():
    return FileResponse("templates/about.html")

@app.get("/contact", response_class=HTMLResponse)
def read_contact():
    return FileResponse("templates/contact.html")

@app.get("/random_recommendation")
def read_random_recommendation():
    return {1: "Hello World"}