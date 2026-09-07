import pytest

from authority_cut.bank_ecp_bridge import evaluate_bank_ecp_bridge
from authority_cut.engine import ControlPlane
from authority_cut.model import EvidenceVerdict, Status
from authority_cut.tools import VendorTools
from authority_cut.workflow import bank_vendor_onboarding_graph


def make() -> ControlPlane:
    return ControlPlane(bank_vendor_onboarding_graph(), VendorTools.memory())


def test_supported_dora_vendor_responsibility_is_pass():
    decision = evaluate_bank_ecp_bridge("DORA_VENDOR_RESPONSIBILITY_SUPPORTED")
    assert decision.verdict == EvidenceVerdict.PASS
    assert decision.source_locator == "Regulation (EU) 2022/2554, Article 28(1)(a)"
    assert decision.evidence_class == "DEVELOPMENT_ONLY"


def test_reversed_responsibility_claim_is_hold():
    decision = evaluate_bank_ecp_bridge("DORA_VENDOR_RESPONSIBILITY_REVERSED")
    assert decision.verdict == EvidenceVerdict.HOLD
    assert "MATERIAL_CITATION_MISMATCH" in decision.reasons


def test_bridge_has_stable_nonempty_digest():
    decision = evaluate_bank_ecp_bridge("DORA_VENDOR_RESPONSIBILITY_SUPPORTED")
    assert len(decision.digest) == 64


def test_vendor_risk_cannot_be_approved_before_evidence_pass():
    plane = make()
    plane.execute_autonomous()
    with pytest.raises(ValueError, match="evidence gate"):
        plane.decide("vendor-risk", True, "reviewed")


def test_pass_evidence_unlocks_human_vendor_risk_decision():
    plane = make()
    plane.execute_autonomous()
    plane.apply_evidence(
        "vendor-risk",
        evaluate_bank_ecp_bridge("DORA_VENDOR_RESPONSIBILITY_SUPPORTED"),
    )
    surface = {item["bundle_id"]: item for item in plane.decision_surface()}
    assert surface["vendor-risk"]["evidence_verdict"] == "PASS"
    assert surface["vendor-risk"]["evidence_ready"] is True
    assert surface["vendor-risk"]["ready"] is True
    plane.decide("vendor-risk", True, "reviewed")


def test_non_pass_evidence_before_approval_keeps_authority_blocked():
    plane = make()
    plane.execute_autonomous()
    affected = plane.apply_evidence(
        "vendor-risk",
        evaluate_bank_ecp_bridge("DORA_VENDOR_RESPONSIBILITY_REVERSED"),
    )
    assert affected == set()
    with pytest.raises(ValueError, match="evidence gate"):
        plane.decide("vendor-risk", True, "reviewed")
    assert plane.state.status["activate"] == Status.BLOCKED


def test_pass_to_hold_invalidates_stale_authority_and_rolls_back_only_affected_work():
    plane = make()
    plane.execute_autonomous()
    plane.apply_evidence(
        "vendor-risk",
        evaluate_bank_ecp_bridge("DORA_VENDOR_RESPONSIBILITY_SUPPORTED"),
    )
    plane.decide("vendor-risk", True, "reviewed")
    plane.execute_authorized()
    plane.decide("payment-release", True, "reviewed")
    plane.execute_authorized()

    affected = plane.apply_evidence(
        "vendor-risk",
        evaluate_bank_ecp_bridge("DORA_VENDOR_RESPONSIBILITY_REVERSED"),
    )

    assert "activate" in affected
    assert plane.state.status["payments"] == Status.ROLLED_BACK
    assert plane.state.status["transmit"] == Status.INVALIDATED
    for safe in ["collect", "tax_check", "bank_check", "draft", "followup"]:
        assert plane.state.status[safe] == Status.EXECUTED
