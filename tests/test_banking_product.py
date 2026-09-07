from fastapi.testclient import TestClient

from authority_cut.api import app as control_app
from authority_cut.live_proof import run_live_strands_proof
from authority_cut.public_app import app as public_app

SAFE_ACTIONS = ("collect", "tax_check", "bank_check", "draft", "followup")


def test_control_api_evidence_correction_drives_selective_rollback():
    client = TestClient(control_app)
    assert client.post("/api/reset").status_code == 200

    safe = client.post("/api/run-safe")
    assert safe.status_code == 200
    assert safe.json()["evidence"]["vendor-risk"]["verdict"] == "PASS"

    vendor = client.post(
        "/api/decisions/vendor-risk",
        json={"approved": True, "rationale": "Vendor-risk reviewer approves"},
    )
    assert vendor.status_code == 200

    payment = client.post(
        "/api/decisions/payment-release",
        json={"approved": True, "rationale": "Payment operations approves profile setup"},
    )
    assert payment.status_code == 200

    corrected = client.post("/api/evidence/vendor-risk/corrected")
    assert corrected.status_code == 200
    payload = corrected.json()
    assert payload["evidence"]["vendor-risk"]["verdict"] == "HOLD"
    assert "MATERIAL_CITATION_MISMATCH" in payload["evidence"]["vendor-risk"]["reasons"]
    assert payload["status"]["payments"] == "ROLLED_BACK"
    assert payload["status"]["transmit"] == "INVALIDATED"
    for action_id in SAFE_ACTIONS:
        assert payload["status"][action_id] == "EXECUTED"


def test_live_strands_proof_uses_evidence_change_as_the_correction_trigger():
    proof = run_live_strands_proof()
    assert proof["correction_trigger"] == "BANK_ECP_EVIDENCE_CHANGE"
    assert proof["bank_ecp_evidence_after_correction"]["verdict"] == "HOLD"
    assert proof["authority_mutation_tools"] == []
    assert proof["safe_actions_preserved"] == 5
    assert proof["protected_reversible_effects_rolled_back"] == 6
    assert proof["irreversible_transmit_after_correction"] == "INVALIDATED"


def test_public_first_screen_is_bank_story_before_technical_evidence():
    html = TestClient(public_app).get("/").text
    assert "Bank vendor onboarding" in html
    assert "Onboard a vendor without giving the AI the final say" in html
    assert "The AI handles routine vendor work" in html
    assert "payment stays blocked" in html
    assert "Evidence changes" in html
    assert "Technical evidence" in html
    assert html.index("Onboard a vendor without giving the AI the final say") < html.index("Technical evidence")
