"""Thin AgentCore Runtime adapter for the verified Authority Cut proof.

The adapter does not add authority or model capabilities. It wraps the existing
Strands proof so AgentCore Runtime can host and invoke the same control semantics.
"""
from __future__ import annotations

from collections.abc import Callable
from typing import Any


def build_agentcore_response(
    run_proof: Callable[[], dict[str, Any]], payload: dict[str, Any] | None = None
) -> dict[str, Any]:
    proof = dict(run_proof())
    proof["agentcore_runtime_adapter"] = "BEDROCK_AGENTCORE_DIRECT_CODE"
    proof["agentcore"] = "RUNTIME_ADAPTER_EXECUTED"
    proof["request"] = dict(payload or {})
    return proof
