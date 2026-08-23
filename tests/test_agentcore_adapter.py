from authority_cut.agentcore_adapter import build_agentcore_response


def test_agentcore_response_preserves_control_proof_and_marks_runtime_adapter():
    proof = {
        "execution": "REAL_STRANDS_AGENT_LOOP_DETERMINISTIC_MODEL",
        "authority_mutation_tools": [],
        "authority_boundary": "EXTERNAL_HUMAN_ONLY",
        "safe_actions_preserved": 5,
        "protected_reversible_effects_rolled_back": 6,
        "irreversible_transmit_after_correction": "INVALIDATED",
        "foundation_model_invocation": "UNVERIFIED",
        "agentcore": "UNVERIFIED",
    }

    result = build_agentcore_response(lambda: proof, {"prompt": "judge-proof"})

    assert result["execution"] == "REAL_STRANDS_AGENT_LOOP_DETERMINISTIC_MODEL"
    assert result["authority_mutation_tools"] == []
    assert result["authority_boundary"] == "EXTERNAL_HUMAN_ONLY"
    assert result["safe_actions_preserved"] == 5
    assert result["protected_reversible_effects_rolled_back"] == 6
    assert result["irreversible_transmit_after_correction"] == "INVALIDATED"
    assert result["foundation_model_invocation"] == "UNVERIFIED"
    assert result["agentcore_runtime_adapter"] == "BEDROCK_AGENTCORE_DIRECT_CODE"
    assert result["agentcore"] == "RUNTIME_ADAPTER_EXECUTED"
    assert result["request"] == {"prompt": "judge-proof"}
