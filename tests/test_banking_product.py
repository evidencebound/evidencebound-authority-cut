from pathlib import Path

from fastapi.testclient import TestClient

from authority_cut.api import app as control_app

ROOT = Path(__file__).resolve().parents[1]
SAFE_ACTIONS = ("collect", "tax_check", "bank_check", "draft", "followup")
PUBLIC_APP_SOURCE = (ROOT / "src" / "authority_cut" / "public_app.py").read_text(encoding="utf-8")
README = (ROOT / "README.md").read_text(encoding="utf-8")
BANK_ECP_BRIDGE_DOC = ROOT / "docs" / "bank-ecp-bridge.md"


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


def test_public_first_screen_source_is_bank_story_before_technical_evidence():
    assert "Bank vendor onboarding" in PUBLIC_APP_SOURCE
    assert "Onboard a vendor without giving the AI the final say" in PUBLIC_APP_SOURCE
    assert "The AI handles routine vendor work" in PUBLIC_APP_SOURCE
    assert "payment stays blocked" in PUBLIC_APP_SOURCE
    assert "Evidence changes" in PUBLIC_APP_SOURCE
    assert "Technical evidence" in PUBLIC_APP_SOURCE
    assert PUBLIC_APP_SOURCE.index("Onboard a vendor without giving the AI the final say") < PUBLIC_APP_SOURCE.index("Technical evidence")


def test_readme_opens_with_the_bank_problem_before_engineering_terms():
    canonical = (
        "A bank lets an AI onboard a vendor. The AI does the routine work. "
        "A human approves the risky decision. If the evidence changes, affected work "
        "is undone and payment stays blocked."
    )
    assert canonical in README[:1800]
    assert "third-party risk" in README[:1800].lower()
    assert README.index(canonical) < README.index("semantic authority")
    assert "BANK-ECP" in README[:2600]


def test_bank_ecp_bridge_doc_keeps_the_evidence_boundary_explicit():
    assert BANK_ECP_BRIDGE_DOC.exists()
    text = BANK_ECP_BRIDGE_DOC.read_text(encoding="utf-8")
    assert "DEVELOPMENT_ONLY" in text
    assert "NOT_FORMAL_BENCHMARK_EVIDENCE" in text
    assert "No model-performance result is claimed" in text
    assert "Regulation (EU) 2022/2554, Article 28(1)(a)" in text
