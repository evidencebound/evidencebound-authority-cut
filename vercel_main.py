"""Vercel entrypoint for the public Authority Cut judge service.

The GET acceptance route is intentionally a reset-each-call synthetic proof so remote
verification can exercise the same real Strands loop without persistent side effects.
The judge UI continues to use POST /api/strands-proof.
"""
from authority_cut.public_app import app
from authority_cut.live_proof import run_live_strands_proof


@app.get("/api/strands-proof-get", include_in_schema=False)
def strands_proof_get():
    return run_live_strands_proof()
