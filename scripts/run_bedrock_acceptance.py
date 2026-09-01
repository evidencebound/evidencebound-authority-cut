"""Run the real Amazon Bedrock Authority Cut acceptance and emit safe evidence JSON."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import re
import subprocess
from typing import Any

from authority_cut.bedrock_proof import (
    DEFAULT_BEDROCK_MODEL_ID,
    DEFAULT_BEDROCK_REGION,
    run_bedrock_strands_proof,
)

_SHA40 = re.compile(r"^[0-9a-f]{40}$")
_REAL_WORKFLOW_INVARIANTS: dict[str, Any] = {
    "execution": "REAL_STRANDS_AGENT_LOOP_FOUNDATION_MODEL",
    "provider": "AMAZON_BEDROCK",
    "model_id": DEFAULT_BEDROCK_MODEL_ID,
    "region": DEFAULT_BEDROCK_REGION,
    "foundation_model_invocation": "PASS",
    "acceptance_mode": "REAL_NATIVE_BEDROCK",
    "authority_mutation_tools": [],
    "authority_boundary": "EXTERNAL_HUMAN_ONLY",
    "safe_actions_preserved": 5,
    "protected_reversible_effects_rolled_back": 6,
    "irreversible_transmit_after_correction": "INVALIDATED",
}


def _digest_json(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)
    return sha256(payload.encode("utf-8")).hexdigest()


def _validate_target(*, model_id: str, region: str) -> None:
    if region != DEFAULT_BEDROCK_REGION:
        raise RuntimeError("Bedrock acceptance region must be eu-central-1; fail closed")
    if model_id != DEFAULT_BEDROCK_MODEL_ID:
        raise RuntimeError(
            f"Bedrock acceptance model must be {DEFAULT_BEDROCK_MODEL_ID}; fail closed"
        )


def collect_bedrock_preflight(*, session: Any, model_id: str, region: str) -> dict[str, Any]:
    """Verify AWS identity context and an ACTIVE inference profile without exposing ARNs."""
    _validate_target(model_id=model_id, region=region)
    sts = session.client("sts", region_name=region)
    identity = sts.get_caller_identity()
    identity_binding = {
        "Account": identity.get("Account"),
        "Arn": identity.get("Arn"),
        "UserId": identity.get("UserId"),
    }
    if not all(identity_binding.values()):
        raise RuntimeError("AWS caller identity incomplete; fail closed")

    bedrock = session.client("bedrock", region_name=region)
    profile = bedrock.get_inference_profile(inferenceProfileIdentifier=model_id)
    profile_id = profile.get("inferenceProfileId")
    if profile_id != model_id:
        raise RuntimeError(
            f"Bedrock inference profile ID mismatch: expected {model_id!r}; fail closed"
        )
    if profile.get("status") != "ACTIVE":
        raise RuntimeError("Bedrock inference profile is not ACTIVE; fail closed")

    model_arns = sorted(
        str(item.get("modelArn"))
        for item in profile.get("models", [])
        if item.get("modelArn")
    )
    if not model_arns:
        raise RuntimeError("Bedrock inference profile has no target models; fail closed")

    result: dict[str, Any] = {
        "aws_identity_sha256": _digest_json(identity_binding),
        "inference_profile_id": profile_id,
        "inference_profile_status": profile.get("status"),
        "inference_profile_type": profile.get("type"),
        "inference_profile_model_count": len(model_arns),
        "inference_profile_models_sha256": _digest_json(model_arns),
    }

    response_metadata = profile.get("ResponseMetadata") or {}
    request_id = response_metadata.get("RequestId")
    if request_id:
        result["bedrock_control_request_id"] = str(request_id)
    return result


def _validate_model_response_receipts(workflow: dict[str, Any]) -> None:
    receipts = workflow.get("model_response_receipts")
    if not isinstance(receipts, list) or len(receipts) != 3:
        raise RuntimeError("model response receipts must contain exactly three turns; fail closed")
    expected_phases = ["safe", "vendor-risk", "payment-release"]
    if [item.get("phase") for item in receipts if isinstance(item, dict)] != expected_phases:
        raise RuntimeError("model response receipts have invalid phase order; fail closed")

    hashes: list[str] = []
    for receipt in receipts:
        if not isinstance(receipt, dict):
            raise RuntimeError("model response receipts are malformed; fail closed")
        digest = receipt.get("sha256")
        usage = receipt.get("usage")
        if not isinstance(digest, str) or len(digest) != 64:
            raise RuntimeError("model response receipts require SHA-256 hashes; fail closed")
        if not isinstance(usage, dict) or usage.get("totalTokens", 0) <= 0:
            raise RuntimeError("model response receipts require positive token usage; fail closed")
        hashes.append(digest)
    if len(set(hashes)) != 3:
        raise RuntimeError("model response receipts must contain three distinct responses; fail closed")


def build_evidence_record(
    *,
    git_commit: str,
    accepted_at_utc: str,
    preflight: dict[str, Any],
    workflow: dict[str, Any],
) -> dict[str, Any]:
    if not _SHA40.fullmatch(git_commit):
        raise RuntimeError("acceptance requires an exact 40-character Git SHA")
    if workflow.get("foundation_model_invocation") != "PASS":
        raise RuntimeError("foundation-model workflow did not PASS; fail closed")
    if preflight.get("inference_profile_status") != "ACTIVE":
        raise RuntimeError("Bedrock inference profile preflight did not PASS; fail closed")
    if preflight.get("inference_profile_id") != workflow.get("model_id"):
        raise RuntimeError("Bedrock profile/model mismatch; fail closed")

    for field, expected in _REAL_WORKFLOW_INVARIANTS.items():
        if workflow.get(field) != expected:
            raise RuntimeError(
                f"real Bedrock acceptance invariant failed for {field}; fail closed"
            )
    _validate_model_response_receipts(workflow)

    return {
        "evidence_schema": "authority-cut-bedrock-foundation-model-acceptance/v1",
        "accepted_at_utc": accepted_at_utc,
        "git_commit": git_commit,
        "aws_preflight": dict(preflight),
        "workflow": dict(workflow),
    }


def _git_commit_sha() -> str:
    completed = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    )
    sha = completed.stdout.strip().lower()
    if not _SHA40.fullmatch(sha):
        raise RuntimeError("could not resolve exact 40-character Git SHA; fail closed")
    return sha


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run real native Amazon Bedrock foundation-model acceptance for Authority Cut."
    )
    parser.add_argument("--region", default=DEFAULT_BEDROCK_REGION)
    parser.add_argument("--model-id", default=DEFAULT_BEDROCK_MODEL_ID)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    _validate_target(model_id=args.model_id, region=args.region)

    try:
        import boto3
    except ImportError as exc:
        raise RuntimeError("boto3 unavailable; install the AWS extra; fail closed") from exc

    session = boto3.Session(region_name=args.region)
    preflight = collect_bedrock_preflight(
        session=session,
        model_id=args.model_id,
        region=args.region,
    )
    workflow = run_bedrock_strands_proof(model_id=args.model_id, region=args.region)
    record = build_evidence_record(
        git_commit=_git_commit_sha(),
        accepted_at_utc=datetime.now(timezone.utc).isoformat(timespec="seconds").replace(
            "+00:00", "Z"
        ),
        preflight=preflight,
        workflow=workflow,
    )

    rendered = json.dumps(record, indent=2, sort_keys=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
