from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


__all__ = ["app"]


app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
app.mount("/static", StaticFiles(directory="static"), name="static")

template_response = Jinja2Templates(directory="templates").TemplateResponse


@app.get("/")
def index(request: Request):
    return template_response("index.jinja", {"request": request})
