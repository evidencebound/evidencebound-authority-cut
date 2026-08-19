"""Protected Vercel preview entrypoint for foundation-model acceptance only.

Do not attach this route to the public production alias: each /proof request can incur
AI Gateway model usage. The public judge service remains credential-free.
"""
from __future__ import annotations

from fastapi import FastAPI

from authority_cut.gateway_proof import DEFAULT_GATEWAY_MODEL, run_gateway_strands_proof

app = FastAPI(title="Authority Cut Foundation-Model Acceptance", version="1.0.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "READY_FOR_PROTECTED_ACCEPTANCE",
        "model": DEFAULT_GATEWAY_MODEL,
        "public_route": "DISALLOWED",
        "agentcore": "UNVERIFIED",
    }


@app.get("/proof")
def proof() -> dict:
    return run_gateway_strands_proof()
