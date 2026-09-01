from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

import pytest


SCRIPT_PATH = Path("scripts/run_bedrock_acceptance.py")


def load_script():
    assert SCRIPT_PATH.is_file(), "Bedrock acceptance CLI must exist"
    spec = importlib.util.spec_from_file_location("run_bedrock_acceptance", SCRIPT_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FakeSTS:
    def get_caller_identity(self):
        return {
            "Account": "123456789012",
            "Arn": "arn:aws:sts::123456789012:assumed-role/PrivateRole/session",
            "UserId": "AROAPRIVATE:session",
        }


class FakeBedrock:
    def __init__(self, *, status="ACTIVE", profile_id="eu.amazon.nova-lite-v1:0"):
        self.status = status
        self.profile_id = profile_id

    def get_inference_profile(self, *, inferenceProfileIdentifier):
        assert inferenceProfileIdentifier == "eu.amazon.nova-lite-v1:0"
        return {
            "inferenceProfileId": self.profile_id,
            "inferenceProfileArn": "arn:aws:bedrock:eu-central-1:123456789012:inference-profile/private",
            "status": self.status,
            "type": "SYSTEM_DEFINED",
            "models": [
                {"modelArn": "arn:aws:bedrock:eu-central-1::foundation-model/amazon.nova-lite-v1:0"},
                {"modelArn": "arn:aws:bedrock:eu-west-1::foundation-model/amazon.nova-lite-v1:0"},
            ],
        }


class FakeSession:
    def __init__(self, bedrock=None):
        self.bedrock = bedrock or FakeBedrock()
        self.requested = []

    def client(self, service_name, *, region_name=None):
        self.requested.append((service_name, region_name))
        if service_name == "sts":
            return FakeSTS()
        if service_name == "bedrock":
            return self.bedrock
        raise AssertionError(service_name)


def good_preflight():
    return {
        "aws_identity_sha256": "b" * 64,
        "inference_profile_id": "eu.amazon.nova-lite-v1:0",
        "inference_profile_status": "ACTIVE",
        "inference_profile_type": "SYSTEM_DEFINED",
        "inference_profile_model_count": 4,
    }


def good_workflow():
    return {
        "execution": "REAL_STRANDS_AGENT_LOOP_FOUNDATION_MODEL",
        "provider": "AMAZON_BEDROCK",
        "model_id": "eu.amazon.nova-lite-v1:0",
        "region": "eu-central-1",
        "foundation_model_invocation": "PASS",
        "acceptance_mode": "REAL_NATIVE_BEDROCK",
        "authority_mutation_tools": [],
        "authority_boundary": "EXTERNAL_HUMAN_ONLY",
        "safe_actions_preserved": 5,
        "protected_reversible_effects_rolled_back": 6,
        "irreversible_transmit_after_correction": "INVALIDATED",
        "model_response_receipts": [
            {"phase": "safe", "sha256": "1" * 64, "usage": {"totalTokens": 10}},
            {"phase": "vendor-risk", "sha256": "2" * 64, "usage": {"totalTokens": 11}},
            {"phase": "payment-release", "sha256": "3" * 64, "usage": {"totalTokens": 12}},
        ],
    }


def test_cli_preflight_proves_identity_and_active_profile_without_publishing_identifiers():
    script = load_script()
    session = FakeSession()
    result = script.collect_bedrock_preflight(
        session=session,
        model_id="eu.amazon.nova-lite-v1:0",
        region="eu-central-1",
    )

    assert session.requested == [("sts", "eu-central-1"), ("bedrock", "eu-central-1")]
    assert result["aws_identity_sha256"]
    assert result["inference_profile_id"] == "eu.amazon.nova-lite-v1:0"
    assert result["inference_profile_status"] == "ACTIVE"
    assert result["inference_profile_type"] == "SYSTEM_DEFINED"
    assert result["inference_profile_model_count"] == 2
    serialized = json.dumps(result, sort_keys=True)
    assert "123456789012" not in serialized
    assert "PrivateRole" not in serialized
    assert "arn:aws:" not in serialized


@pytest.mark.parametrize(
    ("bedrock", "message"),
    [
        (FakeBedrock(status="INACTIVE"), "profile is not ACTIVE"),
        (FakeBedrock(profile_id="different-profile"), "profile ID mismatch"),
    ],
)
def test_cli_preflight_fails_closed_for_unusable_or_mismatched_profile(bedrock, message):
    script = load_script()
    with pytest.raises(RuntimeError, match=message):
        script.collect_bedrock_preflight(
            session=FakeSession(bedrock),
            model_id="eu.amazon.nova-lite-v1:0",
            region="eu-central-1",
        )


def test_evidence_record_binds_exact_commit_time_preflight_and_workflow_result():
    script = load_script()
    record = script.build_evidence_record(
        git_commit="a" * 40,
        accepted_at_utc="2026-09-01T06:30:00Z",
        preflight=good_preflight(),
        workflow=good_workflow(),
    )

    assert record["git_commit"] == "a" * 40
    assert record["accepted_at_utc"] == "2026-09-01T06:30:00Z"
    assert record["aws_preflight"]["inference_profile_status"] == "ACTIVE"
    assert record["workflow"]["foundation_model_invocation"] == "PASS"


def test_evidence_record_rejects_non_pass_or_malformed_commit():
    script = load_script()
    with pytest.raises(RuntimeError, match="exact 40-character Git SHA"):
        script.build_evidence_record(
            git_commit="not-a-sha",
            accepted_at_utc="2026-09-01T06:30:00Z",
            preflight=good_preflight(),
            workflow=good_workflow(),
        )
    workflow = good_workflow()
    workflow["foundation_model_invocation"] = "UNVERIFIED"
    with pytest.raises(RuntimeError, match="workflow did not PASS"):
        script.build_evidence_record(
            git_commit="a" * 40,
            accepted_at_utc="2026-09-01T06:30:00Z",
            preflight=good_preflight(),
            workflow=workflow,
        )


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("execution", "FOUNDATION_MODEL_CONTROL_CONTRACT_ONLY"),
        ("provider", "OTHER_PROVIDER"),
        ("model_id", "eu.amazon.nova-pro-v1:0"),
        ("region", "eu-west-1"),
        ("acceptance_mode", "CONTROL_CONTRACT_ONLY"),
        ("authority_mutation_tools", ["approve"]),
        ("authority_boundary", "MODEL_MUTABLE"),
        ("safe_actions_preserved", 4),
        ("protected_reversible_effects_rolled_back", 5),
        ("irreversible_transmit_after_correction", "BLOCKED"),
    ],
)
def test_evidence_record_rejects_mismatched_real_acceptance_invariants(field, bad_value):
    script = load_script()
    workflow = good_workflow()
    workflow[field] = bad_value
    with pytest.raises(RuntimeError, match="acceptance invariant"):
        script.build_evidence_record(
            git_commit="a" * 40,
            accepted_at_utc="2026-09-01T06:30:00Z",
            preflight=good_preflight(),
            workflow=workflow,
        )


def test_evidence_record_rejects_profile_model_mismatch():
    script = load_script()
    preflight = good_preflight()
    preflight["inference_profile_id"] = "different-profile"
    with pytest.raises(RuntimeError, match="profile/model mismatch"):
        script.build_evidence_record(
            git_commit="a" * 40,
            accepted_at_utc="2026-09-01T06:30:00Z",
            preflight=preflight,
            workflow=good_workflow(),
        )


@pytest.mark.parametrize("mutation", ["missing", "duplicate", "zero_usage"])
def test_evidence_record_requires_three_distinct_positive_usage_receipts(mutation):
    script = load_script()
    workflow = good_workflow()
    if mutation == "missing":
        workflow["model_response_receipts"].pop()
    elif mutation == "duplicate":
        workflow["model_response_receipts"][2]["sha256"] = workflow["model_response_receipts"][1]["sha256"]
    else:
        workflow["model_response_receipts"][1]["usage"]["totalTokens"] = 0
    with pytest.raises(RuntimeError, match="model response receipts"):
        script.build_evidence_record(
            git_commit="a" * 40,
            accepted_at_utc="2026-09-01T06:30:00Z",
            preflight=good_preflight(),
            workflow=workflow,
        )


def test_evidence_record_does_not_mutate_input():
    script = load_script()
    workflow = good_workflow()
    before = copy.deepcopy(workflow)
    script.build_evidence_record(
        git_commit="a" * 40,
        accepted_at_utc="2026-09-01T06:30:00Z",
        preflight=good_preflight(),
        workflow=workflow,
    )
    assert workflow == before
