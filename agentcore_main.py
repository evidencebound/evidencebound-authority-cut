"""Amazon Bedrock AgentCore Runtime entrypoint for Authority Cut.

This direct-code adapter hosts the same real Strands SDK proof used by the public
judge path. It does not add model-callable authority mutation capabilities.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from bedrock_agentcore.runtime import BedrockAgentCoreApp

from authority_cut.agentcore_adapter import build_agentcore_response

app = BedrockAgentCoreApp()


@app.entrypoint
def authority_cut_agentcore(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    from authority_cut.live_proof import run_live_strands_proof

    return build_agentcore_response(run_live_strands_proof, payload)


if __name__ == "__main__":
    app.run()
