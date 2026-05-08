import threading
import webbrowser
from contextlib import asynccontextmanager
from typing import Literal

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

import placeholder_registry
import votes as vote_store
from gallery_miner import mine
from prompt_generator import generate
from template_parser import Template, parse_gallery, parse_templates
from template_repo import ensure_repo

GALLERY_CATEGORY = "精选案例"

_templates: dict[str, list[Template]] = {}  # curated templates, keyed by category
_gallery: list[Template] = []               # all gallery examples, flat pool


@asynccontextmanager
async def lifespan(app: FastAPI):
    repo_path = ensure_repo()
    _templates.update(parse_templates(repo_path))
    for items in parse_gallery(repo_path).values():
        _gallery.extend(items)
    placeholder_registry.init(mine(repo_path))
    print(f"Loaded {sum(len(v) for v in _templates.values())} templates + {len(_gallery)} gallery examples")
    yield


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def index():
    return FileResponse("static/index.html")


@app.get("/api/categories")
def categories():
    return list(_templates.keys()) + [GALLERY_CATEGORY]


class VoteRequest(BaseModel):
    template_id: str
    direction: Literal["up", "down"]


@app.post("/api/vote")
def api_vote(req: VoteRequest):
    result = vote_store.record(req.template_id, req.direction)
    return {"template_id": req.template_id, **result}


class GenerateRequest(BaseModel):
    category: str | None = None
    lang: Literal["en", "zh"] = "zh"
    template_id: str | None = None
    has_image: bool = False


@app.post("/api/generate")
def api_generate(req: GenerateRequest):
    if not _templates:
        raise HTTPException(status_code=503, detail="Templates not loaded")
    votes = vote_store.load()
    try:
        prompt, segments, template = generate(
            _templates, req.lang, req.category, req.template_id, req.has_image,
            gallery=_gallery if req.category in (None, GALLERY_CATEGORY) else [],
            votes=votes,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    counts = vote_store.get_info(template.id, votes)
    return {
        "prompt": prompt,
        "segments": segments,
        "template_id": template.id,
        "category": template.category,
        "template_name": template.name,
        "up": counts["up"],
        "down": counts["down"],
    }


def _open_browser():
    webbrowser.open("http://localhost:8000")


if __name__ == "__main__":
    threading.Timer(0.5, _open_browser).start()
    uvicorn.run(app, host="127.0.0.1", port=8000)
