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


def _digest_json(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)
    return sha256(payload.encode("utf-8")).hexdigest()


def collect_bedrock_preflight(*, session: Any, model_id: str, region: str) -> dict[str, Any]:
    """Verify AWS identity context and an ACTIVE inference profile without exposing ARNs."""
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

    return {
        "evidence_schema": "authority-cut-bedrock-foundation-model-acceptance/v1",
        "accepted_at_utc": accepted_at_utc,
        "git_commit": git_commit,
        "aws_preflight": preflight,
        "workflow": workflow,
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
    if args.region != DEFAULT_BEDROCK_REGION:
        raise RuntimeError("Bedrock acceptance region must be eu-central-1; fail closed")

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
