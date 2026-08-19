"""No-network CI contract for the optional Vercel AI Gateway proof."""
from __future__ import annotations

import os

for name in ("AI_GATEWAY_API_KEY", "VERCEL_OIDC_TOKEN"):
    os.environ.pop(name, None)

from fastapi.testclient import TestClient
from authority_cut.gateway_proof import DEFAULT_GATEWAY_MODEL, GATEWAY_BASE_URL, run_gateway_strands_proof
from authority_cut.strands_app import STRANDS_TOOL_NAMES
from gateway_preview import app as preview_app
from strands.models.openai import OpenAIModel

assert DEFAULT_GATEWAY_MODEL == "alibaba/qwen3.5-flash"
assert GATEWAY_BASE_URL == "https://ai-gateway.vercel.sh/v1"
assert STRANDS_TOOL_NAMES == (
    "execute_safe_vendor_work",
    "get_authority_cut",
    "execute_authorized_vendor_work",
)
assert OpenAIModel is not None

health = TestClient(preview_app).get("/health")
assert health.status_code == 200
assert health.json() == {
    "status": "READY_FOR_PROTECTED_ACCEPTANCE",
    "model": "alibaba/qwen3.5-flash",
    "public_route": "DISALLOWED",
    "agentcore": "UNVERIFIED",
}

try:
    run_gateway_strands_proof()
except RuntimeError as exc:
    assert "credential unavailable" in str(exc)
else:
    raise AssertionError("gateway proof must fail closed when no runtime credential exists")

print("GATEWAY_FOUNDATION_MODEL_CONTRACT=PASS_NO_NETWORK")
