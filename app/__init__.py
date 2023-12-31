from typing import Literal, Optional, Annotated

from http.client import responses

from fastapi import FastAPI, Depends
from fastapi.params import Query
from fastapi.responses import RedirectResponse, PlainTextResponse
from fastapi.requests import Request
from fastapi.exceptions import HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from starlette.status import HTTP_418_IM_A_TEAPOT

from .settings import settings

__all__ = ["app"]


app = FastAPI(debug=settings.debug, docs_url=None, redoc_url=None, openapi_url=None)
app.mount("/static", StaticFiles(directory="static"), name="static")

if settings.production:
    app.add_middleware(HTTPSRedirectMiddleware)
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.allowed_hosts)
    app.add_middleware(GZipMiddleware, minimum_size=1000)


@app.exception_handler(HTTPException)
def http_exception_handler(request: Request, exc: HTTPException):
    accept = request.headers.get("accept", "*/*")

    if "text/html" in accept:
        context = {
            "request": request,
            "status_code": exc.status_code,
            "status_message": responses[exc.status_code],
            "detail": exc.detail
        }
        return template_response("error.jinja", context=context, status_code=exc.status_code)
    else:
        return PlainTextResponse(status_code=exc.status_code, content=exc.detail)


def base_context(request: Request):
    return {"base_url": str(settings.base_url)}


def name_context(request: Request):
    first_name = "Rostyslav"
    last_name = "Bohomaz"
    return {
        "short_name": "Rosty",
        "first_name": first_name,
        "last_name": last_name,
        "display_name": f"{first_name} {last_name}",
    }


template_response = Jinja2Templates(
    directory="templates",
    context_processors=[base_context, name_context],
    trim_blocks=True,
    lstrip_blocks=True
).TemplateResponse


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
        return template_response("index.jinja", {
            "request": request,
            "years_old": years_old,
        })
    else:
        response = RedirectResponse(request.headers.get("referer", "/"))
        response.set_cookie("theme", theme)
        return response


@app.get("/about")
def about(request: Request):
    return template_response("about.jinja", {"request": request})


@app.get("/pot")
def pot(request: Request, kind: Literal["coffee", "tea"] = Query("coffee", alias="type")):
    if kind == "coffee":
        raise HTTPException(status_code=HTTP_418_IM_A_TEAPOT, detail="Cannot brew coffee in a teapot.")
    else:
        return template_response("pot.jinja", {"request": request, "kind": kind})
