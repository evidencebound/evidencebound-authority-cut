"""CI contract for the deployable Amazon Bedrock AgentCore Runtime entrypoint."""
from __future__ import annotations

from agentcore_main import authority_cut_agentcore


def main() -> int:
    result = authority_cut_agentcore({"prompt": "CI AgentCore judge proof"})
    assert result["execution"] == "REAL_STRANDS_AGENT_LOOP_DETERMINISTIC_MODEL"
    assert result["authority_mutation_tools"] == []
    assert result["authority_boundary"] == "EXTERNAL_HUMAN_ONLY"
    assert result["safe_actions_preserved"] == 5
    assert result["protected_reversible_effects_rolled_back"] == 6
    assert result["irreversible_transmit_after_correction"] == "INVALIDATED"
    assert result["foundation_model_invocation"] == "UNVERIFIED"
    assert result["agentcore_runtime_adapter"] == "BEDROCK_AGENTCORE_DIRECT_CODE"
    assert result["agentcore"] == "RUNTIME_ADAPTER_EXECUTED"
    print("AGENTCORE_DIRECT_CODE_CONTRACT=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
