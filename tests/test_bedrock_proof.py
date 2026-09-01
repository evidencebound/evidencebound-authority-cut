from __future__ import annotations

import importlib
import importlib.util
import json
from types import SimpleNamespace

import pytest

from authority_cut.strands_app import (
    execute_authorized_vendor_work,
    execute_safe_vendor_work,
    get_authority_cut,
)


EXPECTED_TOOLS = (
    "execute_safe_vendor_work",
    "get_authority_cut",
    "execute_authorized_vendor_work",
)


def bedrock_proof():
    spec = importlib.util.find_spec("authority_cut.bedrock_proof")
    assert spec is not None, "authority_cut.bedrock_proof must exist"
    return importlib.import_module("authority_cut.bedrock_proof")


class ScriptedFoundationAgent:
    """Model stand-in only; all control semantics execute through real Authority Cut tools."""

    def __init__(self) -> None:
        self.calls = 0

    def __call__(self, prompt: str):
        self.calls += 1
        if self.calls == 1:
            execute_safe_vendor_work()
            get_authority_cut()
            text = "safe phase complete; external vendor-risk authority required"
        elif self.calls == 2:
            execute_authorized_vendor_work()
            get_authority_cut()
            text = "vendor-risk phase complete; external payment-release authority required"
        elif self.calls == 3:
            execute_authorized_vendor_work()
            get_authority_cut()
            text = "payment-release phase complete; external first-funds authority required"
        else:
            raise AssertionError(f"unexpected model call {self.calls}: {prompt}")
        return SimpleNamespace(
            stop_reason="end_turn",
            metrics=SimpleNamespace(
                accumulated_usage={"inputTokens": 10 + self.calls, "outputTokens": 5, "totalTokens": 15 + self.calls}
            ),
            __str__=lambda self: text,
            text=text,
        )


class ScriptedStringAgent:
    def __init__(self) -> None:
        self.calls = 0

    def __call__(self, prompt: str):
        self.calls += 1
        if self.calls == 1:
            execute_safe_vendor_work()
            get_authority_cut()
        elif self.calls == 2:
            execute_authorized_vendor_work()
            get_authority_cut()
        elif self.calls == 3:
            execute_authorized_vendor_work()
            get_authority_cut()
        else:
            raise AssertionError("unexpected extra invocation")
        return f"phase-{self.calls}-foundation-response"


def test_bedrock_contract_uses_verified_eu_nova_lite_profile_and_existing_tool_surface():
    bp = bedrock_proof()
    assert bp.DEFAULT_BEDROCK_REGION == "eu-central-1"
    assert bp.DEFAULT_BEDROCK_MODEL_ID == "eu.amazon.nova-lite-v1:0"
    assert tuple(bp.STRANDS_TOOL_NAMES) == EXPECTED_TOOLS
    assert bp.AUTHORITY_MUTATION_TOOLS == ()
    assert all("approve" not in name and "revoke" not in name for name in bp.STRANDS_TOOL_NAMES)


def test_bedrock_agent_builder_wires_model_profile_and_shared_strands_builder(monkeypatch):
    bp = bedrock_proof()
    captured = {}

    class DummyBedrockModel:
        def __init__(self, **kwargs):
            captured["model_kwargs"] = kwargs

    sentinel_agent = object()

    def fake_build_agent(*, model):
        captured["agent_model"] = model
        return sentinel_agent

    monkeypatch.setattr(bp, "_load_bedrock_model_class", lambda: DummyBedrockModel)
    monkeypatch.setattr(bp, "build_agent", fake_build_agent)

    agent = bp.build_bedrock_agent(
        model_id="eu.amazon.nova-lite-v1:0",
        region="eu-central-1",
    )

    assert agent is sentinel_agent
    assert captured["model_kwargs"]["model_id"] == "eu.amazon.nova-lite-v1:0"
    assert captured["model_kwargs"]["region_name"] == "eu-central-1"
    assert captured["model_kwargs"]["temperature"] == 0.0
    assert captured["agent_model"].__class__ is DummyBedrockModel
    assert tuple(bp.STRANDS_TOOL_NAMES) == EXPECTED_TOOLS


@pytest.mark.parametrize(
    ("model_id", "region"),
    [("", "eu-central-1"), ("eu.amazon.nova-lite-v1:0", "")],
)
def test_missing_model_or_region_configuration_fails_closed(model_id, region):
    bp = bedrock_proof()
    with pytest.raises(RuntimeError, match="configuration unavailable.*fail closed"):
        bp.build_bedrock_agent(model_id=model_id, region=region)


def test_missing_aws_credentials_fails_closed_before_model_invocation(monkeypatch):
    bp = bedrock_proof()
    monkeypatch.setattr(bp, "_aws_credentials_available", lambda: False)
    with pytest.raises(RuntimeError, match="AWS credentials unavailable.*fail closed"):
        bp.run_bedrock_strands_proof(
            model_id="eu.amazon.nova-lite-v1:0",
            region="eu-central-1",
        )


def test_foundation_acceptance_preserves_external_authority_and_correction_semantics():
    bp = bedrock_proof()
    result = bp.run_foundation_model_acceptance(
        ScriptedStringAgent(),
        provider="TEST_FOUNDATION_PROVIDER",
        model_id="test-model",
        region="eu-central-1",
        require_model_metrics=False,
    )

    assert result["execution"] == "REAL_STRANDS_AGENT_LOOP_FOUNDATION_MODEL"
    assert result["authority_mutation_tools"] == []
    assert result["authority_boundary"] == "EXTERNAL_HUMAN_ONLY"
    assert result["safe_actions_preserved"] == 5
    assert result["protected_reversible_effects_rolled_back"] == 6
    assert result["irreversible_transmit_after_correction"] == "INVALIDATED"
    assert result["foundation_model_invocation"] == "PASS"
    assert result["phases"][0]["status"]["activate"] == "BLOCKED"
    assert result["phases"][1]["status"]["activate"] == "EXECUTED"
    assert result["phases"][1]["status"]["payments"] == "BLOCKED"
    assert result["phases"][2]["status"]["remittance"] == "EXECUTED"
    assert result["phases"][2]["status"]["transmit"] == "BLOCKED"
    assert result["phases"][2]["ready_authorities"] == ["first-funds"]
    assert result["phases"][3]["status"]["transmit"] == "INVALIDATED"
    for action_id in ("activate", "erp_sync", "purchasing", "payments", "terms", "remittance"):
        assert result["phases"][3]["status"][action_id] == "ROLLED_BACK"
    for action_id in ("collect", "tax_check", "bank_check", "draft", "followup"):
        assert result["phases"][3]["status"][action_id] == "EXECUTED"


def test_real_pass_requires_nonzero_model_usage_receipts():
    bp = bedrock_proof()
    with pytest.raises(AssertionError, match="model usage metadata"):
        bp._model_response_receipt("safe", "plain string response", require_metrics=True)

    response = SimpleNamespace(
        stop_reason="end_turn",
        metrics=SimpleNamespace(accumulated_usage={"inputTokens": 12, "outputTokens": 4, "totalTokens": 16}),
    )
    response.__class__.__str__ = lambda self: "bedrock response"
    receipt = bp._model_response_receipt("safe", response, require_metrics=True)
    assert receipt["sha256"]
    assert receipt["usage"]["totalTokens"] == 16
    assert receipt["stop_reason"] == "end_turn"


def test_acceptance_records_three_separate_response_hashes_without_raw_model_content():
    bp = bedrock_proof()
    result = bp.run_foundation_model_acceptance(
        ScriptedStringAgent(),
        provider="TEST_FOUNDATION_PROVIDER",
        model_id="test-model",
        region="eu-central-1",
        require_model_metrics=False,
    )
    receipts = result["model_response_receipts"]
    assert [r["phase"] for r in receipts] == ["safe", "vendor-risk", "payment-release"]
    assert len({r["sha256"] for r in receipts}) == 3
    serialized = json.dumps(result, sort_keys=True)
    assert "phase-1-foundation-response" not in serialized
    assert "phase-2-foundation-response" not in serialized
    assert "phase-3-foundation-response" not in serialized


def test_acceptance_output_never_echoes_aws_credentials(monkeypatch):
    bp = bedrock_proof()
    secrets = {
        "AWS_ACCESS_KEY_ID": "AKIATESTSENTINEL1234",
        "AWS_SECRET_ACCESS_KEY": "secret-test-sentinel-value",
        "AWS_SESSION_TOKEN": "session-test-sentinel-value",
    }
    for key, value in secrets.items():
        monkeypatch.setenv(key, value)

    result = bp.run_foundation_model_acceptance(
        ScriptedStringAgent(),
        provider="TEST_FOUNDATION_PROVIDER",
        model_id="test-model",
        region="eu-central-1",
        require_model_metrics=False,
    )
    serialized = json.dumps(result, sort_keys=True)
    for secret in secrets.values():
        assert secret not in serialized
