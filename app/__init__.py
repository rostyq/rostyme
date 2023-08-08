from typing import Literal, Optional, Annotated

from fastapi import FastAPI, Depends
from fastapi.params import Query
from fastapi.responses import RedirectResponse
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


__all__ = ["app"]


app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
app.mount("/static", StaticFiles(directory="static"), name="static")

template_response = Jinja2Templates(directory="templates", trim_blocks=True, lstrip_blocks=True).TemplateResponse


def get_years_old():
    from datetime import datetime, timezone, timedelta

    tz = timezone(offset=timedelta(hours=+3), name="Kyiv")
    
    return (datetime.now(tz) - datetime(1996, 7, 30, tzinfo=tz)).days // 365


@app.get("/")
def index(
    request: Request,
    years_old: Annotated[int, Depends(get_years_old)],
    theme: Optional[Literal["light", "dark"]] = Query(None),
):
    if theme is None:
        return template_response("index.jinja", {"request": request, "years_old": years_old})
    else:
        response = RedirectResponse(request.headers.get("referer", "/"))
        response.set_cookie("theme", theme)
        return response


@app.get("/about")
def about(request: Request):
    return template_response("about.jinja", {"request": request})
