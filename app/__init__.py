from typing import Literal, Optional

from fastapi import FastAPI
from fastapi.params import Query
from fastapi.responses import RedirectResponse
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


__all__ = ["app"]


app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
app.mount("/static", StaticFiles(directory="static"), name="static")

template_response = Jinja2Templates(directory="templates", trim_blocks=True, lstrip_blocks=True).TemplateResponse


@app.get("/")
def index(request: Request, theme: Optional[Literal["light", "dark"]] = Query(None)):
    if theme is None:
        return template_response("index.jinja", {"request": request})
    else:
        response = RedirectResponse("/")
        response.set_cookie("theme", theme)
        return response

