# BANK-ECP Human Control Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make BANK-ECP evidence load-bearing in Authority Cut's banking vendor-onboarding flow, then rewrite the live product and public narrative so a judge sees human value before architecture.

**Architecture:** Add a small development-only BANK-ECP bridge inside the public Authority Cut repository rather than depending on the private benchmark runtime. A `vendor-risk` decision bundle will require an evidence gate to be `PASS`; applying `HOLD` or `ABSTAIN` after approval invalidates stale authority and reuses the existing selective rollback path. The live UI will expose the human banking sequence first while preserving existing Strands/AWS truth endpoints and tool boundaries.

**Tech Stack:** Python 3.11-3.13, FastAPI, pytest, Strands Agents SDK 1.52.0, GitHub Actions, Vercel, Devpost, Google Slides for all submission/YouTube visual assets.

**Spec:** `docs/superpowers/specs/2026-09-07-bank-ecp-human-control-design.md`

## Global Constraints

- Keep human authority mutation outside the model-callable Strands tool surface.
- Do not add approve, revoke, correct-authority, or restore-authority tools to `STRANDS_TOOL_NAMES`.
- BANK-ECP bridge evidence is `DEVELOPMENT_ONLY` / `NOT_FORMAL_BENCHMARK_EVIDENCE`.
- Model confidence never creates authority.
- Preserve historical native Bedrock PASS and AgentCore historical UNVERIFIED foundation-model boundaries exactly.
- Preserve selective rollback, unrelated safe work, and irreversible first-funds gating.
- Do not expose private BANK-ECP benchmark internals; publish only the sanitized DORA bridge fixture.
- Public legal wording must stay within the verified DORA Article 28(1)(a) proposition.
- Thumbnail, YouTube images, and hackathon visual assets must be created only with Google Slides.
- Do not update Devpost until code, CI, production, and final copy are verified.

---

### Task 1: BANK-ECP evidence model and deterministic bridge

**Files:**
- Create: `tests/test_bank_ecp_bridge.py`
- Create: `src/authority_cut/bank_ecp_bridge.py`
- Modify: `src/authority_cut/model.py`

**Interfaces:**
- Produces `EvidenceVerdict(str, Enum)` with `PASS`, `HOLD`, `ABSTAIN`.
- Produces immutable `EvidenceDecision` with `gate_id`, `case_id`, `verdict`, `reasons`, `source_locator`, `evidence_class`, `digest`.
- Produces `evaluate_bank_ecp_bridge(case_id: str) -> EvidenceDecision`.
- Supported public cases: `DORA_VENDOR_RESPONSIBILITY_SUPPORTED` and `DORA_VENDOR_RESPONSIBILITY_REVERSED`.

- [ ] **Step 1: Write failing bridge tests**

```python
from authority_cut.bank_ecp_bridge import evaluate_bank_ecp_bridge
from authority_cut.model import EvidenceVerdict


def test_supported_dora_vendor_responsibility_is_pass():
    d = evaluate_bank_ecp_bridge("DORA_VENDOR_RESPONSIBILITY_SUPPORTED")
    assert d.verdict == EvidenceVerdict.PASS
    assert d.source_locator == "Regulation (EU) 2022/2554, Article 28(1)(a)"
    assert d.evidence_class == "DEVELOPMENT_ONLY"


def test_reversed_responsibility_claim_is_hold():
    d = evaluate_bank_ecp_bridge("DORA_VENDOR_RESPONSIBILITY_REVERSED")
    assert d.verdict == EvidenceVerdict.HOLD
    assert "MATERIAL_CITATION_MISMATCH" in d.reasons


def test_bridge_has_stable_nonempty_digest():
    d = evaluate_bank_ecp_bridge("DORA_VENDOR_RESPONSIBILITY_SUPPORTED")
    assert len(d.digest) == 64
```

- [ ] **Step 2: Push RED commit and verify CI failure**

Expected failing command in GitHub Actions deterministic-kernel job:

```bash
python -m pytest -q tests/test_bank_ecp_bridge.py
```

Expected failure: import/module/type is missing.

- [ ] **Step 3: Implement minimal evidence types and bridge**

`model.py` additions:

```python
class EvidenceVerdict(str, Enum):
    PASS = "PASS"
    HOLD = "HOLD"
    ABSTAIN = "ABSTAIN"

@dataclass(frozen=True, slots=True)
class EvidenceDecision:
    gate_id: str
    case_id: str
    verdict: EvidenceVerdict
    reasons: tuple[str, ...]
    source_locator: str
    evidence_class: str
    digest: str
```

`bank_ecp_bridge.py` must use a fixed public dictionary and `digest(...)`; unknown case IDs raise `KeyError`. No model call or expected-label substitution is presented as model output.

- [ ] **Step 4: Verify GREEN**

```bash
python -m pytest -q tests/test_bank_ecp_bridge.py
python -m pytest -q
```

Expected: all tests pass.

---

### Task 2: Make evidence load-bearing for vendor-risk authority

**Files:**
- Modify: `tests/test_bank_ecp_bridge.py`
- Modify: `src/authority_cut/model.py`
- Modify: `src/authority_cut/workflow.py`
- Modify: `src/authority_cut/engine.py`

**Interfaces:**
- `DecisionBundle.evidence_gate: str | None = None`.
- `RuntimeState.evidence: dict[str, EvidenceDecision]`.
- `ControlPlane.apply_evidence(bundle_id: str, decision: EvidenceDecision) -> set[str]`.
- `decision_surface()` adds `evidence_gate`, `evidence_verdict`, `evidence_ready`.

- [ ] **Step 1: Write failing runtime tests**

```python
import pytest
from authority_cut.bank_ecp_bridge import evaluate_bank_ecp_bridge
from authority_cut.model import Status


def test_vendor_risk_cannot_be_approved_before_evidence_pass():
    p = make()
    p.execute_autonomous()
    with pytest.raises(ValueError, match="evidence gate"):
        p.decide("vendor-risk", True, "reviewed")


def test_pass_evidence_unlocks_human_vendor_risk_decision():
    p = make()
    p.execute_autonomous()
    p.apply_evidence("vendor-risk", evaluate_bank_ecp_bridge("DORA_VENDOR_RESPONSIBILITY_SUPPORTED"))
    surface = {x["bundle_id"]: x for x in p.decision_surface()}
    assert surface["vendor-risk"]["evidence_verdict"] == "PASS"
    assert surface["vendor-risk"]["ready"] is True
    p.decide("vendor-risk", True, "reviewed")


def test_pass_to_hold_invalidates_stale_authority_and_rolls_back_only_affected_work():
    p = make()
    p.execute_autonomous()
    p.apply_evidence("vendor-risk", evaluate_bank_ecp_bridge("DORA_VENDOR_RESPONSIBILITY_SUPPORTED"))
    p.decide("vendor-risk", True, "reviewed")
    p.execute_authorized()
    p.decide("payment-release", True, "reviewed")
    p.execute_authorized()
    affected = p.apply_evidence("vendor-risk", evaluate_bank_ecp_bridge("DORA_VENDOR_RESPONSIBILITY_REVERSED"))
    assert "activate" in affected
    assert p.state.status["payments"] == Status.ROLLED_BACK
    assert p.state.status["transmit"] == Status.INVALIDATED
    for safe in ["collect", "tax_check", "bank_check", "draft", "followup"]:
        assert p.state.status[safe] == Status.EXECUTED
```

- [ ] **Step 2: Push RED commit and verify targeted failures**

```bash
python -m pytest -q tests/test_bank_ecp_bridge.py
```

Expected: missing evidence-gate behavior.

- [ ] **Step 3: Implement minimal runtime integration**

Rules:

```text
vendor-risk.evidence_gate = BANK_ECP_DORA_VENDOR_RESPONSIBILITY
approved=True requires prereqs executed AND gate verdict PASS
non-PASS evidence applied after approved decision -> invalidate bundle -> selective rollback
non-PASS evidence before approval -> no rollback, approval remains blocked
payment-release and first-funds remain governed by their existing prerequisite/human rules
```

Refactor existing `revoke_bundle` internals into a private invalidation helper only if needed to avoid duplicating compensation logic. Human revoke and evidence invalidation must remain distinguishable in receipts.

- [ ] **Step 4: Verify GREEN and old invariants**

```bash
python -m pytest -q tests/test_bank_ecp_bridge.py tests/test_authority_cut.py
```

Update legacy tests that now require a supported evidence decision before `vendor-risk` approval. Do not weaken assertions about rollback, tool boundaries, or first-funds.

---

### Task 3: Banking API and human-first live product

**Files:**
- Modify: `tests/test_bank_ecp_bridge.py`
- Modify: `src/authority_cut/api.py`
- Modify: `src/authority_cut/public_app.py`
- Modify: `src/authority_cut/live_proof.py` only if the proof workflow must insert the supported evidence gate while preserving output contracts.

**Interfaces:**
- `POST /api/evidence/vendor-risk/supported`
- `POST /api/evidence/vendor-risk/corrected`
- `snapshot()` exposes `evidence`.
- Existing `/health`, `/api/evaluation`, `/api/tool-boundary`, `/api/strands-proof*` remain truthful.

- [ ] **Step 1: Write failing API/product tests**

```python
from fastapi.testclient import TestClient
from authority_cut.api import app


def test_banking_api_evidence_change_drives_rollback():
    c = TestClient(app)
    c.post("/api/reset")
    c.post("/api/run-safe")
    assert c.post("/api/evidence/vendor-risk/supported").json()["evidence"]["vendor-risk"]["verdict"] == "PASS"
    assert c.post("/api/decisions/vendor-risk", json={"approved": True, "rationale": "reviewed"}).status_code == 200
    c.post("/api/decisions/payment-release", json={"approved": True, "rationale": "reviewed"})
    corrected = c.post("/api/evidence/vendor-risk/corrected").json()
    assert corrected["status"]["payments"] == "ROLLED_BACK"
    assert corrected["status"]["transmit"] == "INVALIDATED"


def test_first_screen_is_bank_human_story_before_diagnostics():
    html = TestClient(app).get("/").text
    assert "Onboard a vendor without giving the AI the final say" in html
    assert "The AI handles routine vendor work" in html
    assert "payment stays blocked" in html
    assert html.index("Onboard a vendor") < html.index("Technical evidence")
```

- [ ] **Step 2: Push RED commit and verify failures**

```bash
python -m pytest -q tests/test_bank_ecp_bridge.py
```

- [ ] **Step 3: Implement endpoints and human-first UI**

First screen order:

```text
Bank vendor onboarding
Onboard a vendor without giving the AI the final say.
AI handles routine work -> human approves risky decision -> evidence changes -> affected work undone -> payment blocked
Primary judge button / guided steps
Current human-visible outcome cards
Technical evidence below fold
```

Use concrete labels such as `Routine checks complete`, `Needs your approval`, `Evidence corrected`, `Vendor activation undone`, `Payment blocked`. Keep semantic bundles, hashes, receipts, deterministic provider, AgentCore history, and fixed metrics below `Technical evidence`.

- [ ] **Step 4: Preserve real Strands proof contracts**

If `run_live_strands_proof()` reaches `vendor-risk`, insert the supported BANK-ECP bridge decision before the external-human approval step. Keep `STRANDS_TOOL_NAMES` exactly:

```python
(
    "execute_safe_vendor_work",
    "get_authority_cut",
    "execute_authorized_vendor_work",
)
```

- [ ] **Step 5: Verify GREEN**

```bash
python -m pytest -q
python -m compileall -q src tests scripts agentcore_main.py
python scripts/run_strands_ci_probe.py
python scripts/run_public_strands_surface_probe.py
```

Expected: no tool-boundary regression and the public proof still ends with preserved safe work, rolled-back reversible effects, and invalidated first payment.

---

### Task 4: Human-first README and technical evidence alignment

**Files:**
- Modify: `README.md`
- Modify: `docs/architecture.md`
- Modify: `docs/architecture.mmd`
- Modify: `handoff/AWS_JUDGE_PACK.md` only where product flow description is stale.
- Create: `docs/bank-ecp-bridge.md`

**Interfaces:**
- README opening 150-200 words answers who, problem, product behavior, judge-visible moment.
- `docs/bank-ecp-bridge.md` states source, sanitized cases, development-only status, and no performance claim.

- [ ] **Step 1: Rewrite README opening**

Required canonical sentence appears near top:

```text
A bank lets an AI onboard a vendor. The AI does the routine work. A human approves the risky decision. If the evidence changes, affected work is undone and payment stays blocked.
```

- [ ] **Step 2: Move engineering proof below product story**

Preserve all verified historical statements; do not rewrite PASS/UNVERIFIED evidence into stronger claims.

- [ ] **Step 3: Document the BANK-ECP bridge**

State clearly:

```text
DEVELOPMENT_ONLY
NOT_FORMAL_BENCHMARK_EVIDENCE
No model-performance result is claimed.
Authoritative source: DORA Article 28(1)(a), EUR-Lex.
```

- [ ] **Step 4: Verify text invariants with tests/grep in CI**

```bash
python -m pytest -q
python -m compileall -q src tests scripts agentcore_main.py
```

---

### Task 5: Branch verification, review, merge, production acceptance

**Files:**
- No production file changes unless verification finds a defect.

- [ ] **Step 1: Require full GitHub Actions success on exact feature HEAD**

Verify every job: deterministic kernel matrix, Strands runtime proof, Bedrock contract, AgentCore contract, gateway contract, source snapshot.

- [ ] **Step 2: Review branch diff against spec**

Reject unsupported claims, private BANK-ECP leakage, new authority-mutation tools, or altered historical evidence boundaries.

- [ ] **Step 3: Merge only after review**

Prefer squash merge into `main` after all required checks are green.

- [ ] **Step 4: Verify Vercel production deployment and browser UX**

Acceptance checks:

```text
5 seconds: bank + vendor + AI + human decision + payment protection are obvious
60 seconds: routine work -> approval -> evidence correction -> rollback -> safe work preserved -> payment blocked
5 minutes: Strands/AWS/BANK-ECP evidence available below product story
```

Verify `/health`, banking API path, and live Strands proof on production.

---

### Task 6: Devpost, video decision, and Google Slides-only visuals

**Files/External surfaces:**
- Devpost Authority Cut project
- Google Slides presentation used as source for thumbnail/YouTube/Devpost visual assets
- Existing YouTube video only if replacement materially improves Presentation

- [ ] **Step 1: Rewrite Devpost human-first**

Opening order: bank problem -> user -> product -> magic moment -> business relevance -> Strands/AWS -> BANK-ECP/EvidenceBound -> technical evidence -> limitations.

- [ ] **Step 2: Read back submitted Devpost after update**

Confirm project remains Submitted and required repo/video/architecture/AWS Builder ID fields remain intact.

- [ ] **Step 3: Decide whether video replacement has positive Presentation ROI**

Keep current video unless the new live banking UI materially changes the story enough to justify a re-recording that can be fully reverified before deadline.

- [ ] **Step 4: Create any new visual assets only in Google Slides**

Do not use image generation or Canva. Export the required image(s) from the Google Slides source and use those exact assets for Devpost/YouTube where owner-authorized publishing is available.

- [ ] **Step 5: Final external acceptance and freeze**

Verify current Devpost state, production, CI, README, video URL, visual consistency, and no unsupported claims. Stop when all are aligned or an owner-only publishing action is the sole remaining blocker.
