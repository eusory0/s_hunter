from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

from app.db import init_db
from app.store import list_opportunities

app = FastAPI(title="s_hunter")
templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
def _startup():
    init_db()

@app.get("/api/opportunities")
def api_opps(limit: int = 200):
    return list_opportunities(limit=limit)

@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    opps = list_opportunities(limit=200)
    return templates.TemplateResponse("dashboard.html", {"request": request, "opps": opps})