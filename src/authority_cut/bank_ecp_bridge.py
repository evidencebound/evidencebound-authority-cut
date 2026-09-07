"""Sanitized BANK-ECP development bridge used by the Authority Cut demo.

This module is deliberately narrow: it exposes two development-only DORA
third-party-risk cases and no benchmark internals, formal holdout data, or
model-performance result.
"""
from __future__ import annotations

from .model import EvidenceDecision, EvidenceVerdict, digest

GATE_ID = "BANK_ECP_DORA_VENDOR_RESPONSIBILITY"
SOURCE_LOCATOR = "Regulation (EU) 2022/2554, Article 28(1)(a)"
EVIDENCE_CLASS = "DEVELOPMENT_ONLY"

_CASES: dict[str, dict[str, object]] = {
    "DORA_VENDOR_RESPONSIBILITY_SUPPORTED": {
        "verdict": EvidenceVerdict.PASS,
        "reasons": (),
        "claim": (
            "A financial entity remains responsible for compliance with and the "
            "discharge of its obligations when it uses ICT third-party services."
        ),
    },
    "DORA_VENDOR_RESPONSIBILITY_REVERSED": {
        "verdict": EvidenceVerdict.HOLD,
        "reasons": ("MATERIAL_CITATION_MISMATCH",),
        "claim": (
            "Using an ICT third-party provider transfers the financial entity's "
            "DORA responsibility to that provider."
        ),
    },
}


def evaluate_bank_ecp_bridge(case_id: str) -> EvidenceDecision:
    case = _CASES[case_id]
    payload = {
        "gate_id": GATE_ID,
        "case_id": case_id,
        "verdict": case["verdict"].value,
        "reasons": list(case["reasons"]),
        "claim": case["claim"],
        "source_locator": SOURCE_LOCATOR,
        "evidence_class": EVIDENCE_CLASS,
        "formal_benchmark_evidence": False,
        "model_performance_result": False,
    }
    return EvidenceDecision(
        gate_id=GATE_ID,
        case_id=case_id,
        verdict=case["verdict"],
        reasons=case["reasons"],
        source_locator=SOURCE_LOCATOR,
        evidence_class=EVIDENCE_CLASS,
        digest=digest(payload),
    )
