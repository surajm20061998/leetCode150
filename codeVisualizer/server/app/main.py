from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from httpx import HTTPError

from .executor import run_trace
from .leetcode import fetch_problem
from .models import ProblemRequest, ProblemResponse, TraceRequest


app = FastAPI(title="Code Visualizer API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.get("/api/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/problems/fetch", response_model=ProblemResponse)
async def problem(request: ProblemRequest) -> ProblemResponse:
    try:
        return await fetch_problem(request.url)
    except (ValueError, HTTPError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/trace")
async def trace(request: TraceRequest) -> dict:
    candidate = await run_trace(
        {"code": request.code, "entrypoint": request.entrypoint, "args": request.args}
    )
    reference = None
    if request.reference_code and request.reference_code.strip() != request.code.strip():
        reference = await run_trace(
            {
                "code": request.reference_code,
                "entrypoint": request.entrypoint,
                "args": request.args,
            }
        )
    comparison = None
    if reference:
        comparison = {
            "matches": candidate.get("status") == reference.get("status") == "completed"
            and candidate.get("result") == reference.get("result"),
            "candidate_result": candidate.get("result"),
            "reference_result": reference.get("result"),
        }
    return {"candidate": candidate, "reference": reference, "comparison": comparison}
