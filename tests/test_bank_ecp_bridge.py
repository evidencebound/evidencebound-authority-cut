from authority_cut.bank_ecp_bridge import evaluate_bank_ecp_bridge
from authority_cut.model import EvidenceVerdict


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
