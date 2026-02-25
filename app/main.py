from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

from app.db import init_db
from app.store import list_opportunities, list_high

app = FastAPI(title="s_hunter")
templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
def _startup():
    init_db()

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/api/opportunities")
def api_opps(limit: int = 200, min_score: float | None = None):
    return list_opportunities(limit=limit, min_score=min_score)

@app.get("/api/high")
def api_high(min_score: float = 85.0, limit: int = 200):
    return list_high(min_score=min_score, limit=limit)

@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request, min_score: float | None = None):
    opps = list_opportunities(limit=200, min_score=min_score)
    return templates.TemplateResponse("dashboard.html", {"request": request, "opps": opps, "min_score": min_score})