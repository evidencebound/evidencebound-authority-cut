# Authority Cut — Vercel Production Evidence

Snapshot: 2026-09-07

## Canonical public judge service

- URL: `https://evidencebound-authority-cut.vercel.app`
- Vercel project: `evidencebound-authority-cut`
- project ID: `prj_WPX42JQ08alE6WfuqlS0xA8XpBzT`
- canonical runtime source commit installed by the deployment: `0b200797497aa3cfc85bda897d6b6f7aec221367`
- accepted production deployment: `dpl_74ucSEgzBMmorM9xfSfSPGcfTdkQ`
- framework/runtime: FastAPI / Python 3.12
- region: `iad1`
- build: **PASS**
- deployment state: **READY**
- canonical alias assignment: **PASS** (`aliasError = null`)

The deployment uses a small Vercel entry bundle whose `pyproject.toml` installs `authority-cut-agent` directly from the exact public Git commit above and pins `strands-agents==1.52.0`. The public route remains credential-free and uses the deterministic custom Strands model provider; no Gateway model route is attached to the judge service.

## Human-facing acceptance

The production root returns HTTP 200. Verified first-screen copy includes the hero **“Onboard a vendor without giving the AI the final say.”** The lede explains that the AI handles routine vendor work, a person approves decisions with real compliance or financial risk, and changed evidence causes affected work to be undone while payment stays blocked.

The first screen exposes the end-to-end banking scenario before technical diagnostics. The technical section explicitly labels the BANK-ECP bridge `DEVELOPMENT_ONLY` and does not claim that the public request invokes a foundation model or AgentCore.

## Public acceptance

Verified against the canonical production alias after deployment:

- judge root/UI: **HTTP 200 PASS**
- `/health`: **HTTP 200 PASS**
- `/api/tool-boundary`: **HTTP 200 PASS**
- `/api/strands-proof-get`: **HTTP 200 PASS**
- Vercel runtime error scan after smoke: **no runtime errors found**

`/health` reports:

```text
status = READY
control_kernel = PASS
live_strands_agent_loop = AVAILABLE
live_model_provider = DETERMINISTIC_CUSTOM
foundation_model = UNVERIFIED
agentcore = UNVERIFIED
authority_boundary = EXTERNAL_HUMAN_ONLY
authority_mutation_tools = []
bank_ecp_bridge = DEVELOPMENT_ONLY
```

`/api/tool-boundary` reports exactly three model-callable operational tools:

```text
execute_safe_vendor_work
get_authority_cut
execute_authorized_vendor_work
```

Authority mutation tools remain absent. Human authority arrives through the external human channel, and evidence updates arrive through an external non-model channel.

## Canonical BANK-ECP correction proof

The accepted `/api/strands-proof-get` result includes:

```text
execution = REAL_STRANDS_AGENT_LOOP_DETERMINISTIC_MODEL
model_provider = deterministic-public-proof
authority_mutation_tools = []
authority_boundary = EXTERNAL_HUMAN_ONLY
correction_trigger = BANK_ECP_EVIDENCE_CHANGE
bank_ecp_evidence_before_correction.verdict = PASS
bank_ecp_evidence_after_correction.verdict = HOLD
bank_ecp_evidence_after_correction.reasons = [MATERIAL_CITATION_MISMATCH]
bank_ecp_evidence_after_correction.evidence_class = DEVELOPMENT_ONLY
safe_actions_preserved = 5
protected_reversible_effects_rolled_back = 6
irreversible_transmit_after_correction = INVALIDATED
foundation_model_invocation = UNVERIFIED
agentcore = UNVERIFIED
receipt_count = 16
```

The public bridge uses the source locator `Regulation (EU) 2022/2554, Article 28(1)(a)`. It is a sanitized development fixture, not formal held-out BANK-ECP benchmark evidence and not a model-performance result.

## Live four-phase banking state proof

### Phase 1 — routine work and evidence check

Five safe vendor-onboarding actions are `EXECUTED`. The BANK-ECP development gate is `PASS`. `vendor-risk` is ready for the human; later payment authorities are not yet ready.

### Phase 2 — external vendor-risk approval

The human approval is applied outside the Strands model tool set. The agent resumes only work authorized by that recorded decision. Vendor activation, ERP synchronization and purchasing execute; payment-profile work remains gated until its own human decision is ready.

### Phase 3 — protected setup complete

After external `payment-release` approval, payment profile, terms and remittance preview execute. The separate first-funds decision becomes ready, while irreversible `transmit` remains `BLOCKED` because no first-funds authority is granted.

### Phase 4 — evidence changes

The BANK-ECP development evidence changes `PASS → HOLD`. This invalidates the stale vendor-risk authority. Six already-executed reversible protected descendants become `ROLLED_BACK`; the pending irreversible transmit becomes `INVALIDATED`; all five unrelated safe actions remain `EXECUTED`.

The trigger is an evidence change, not a model action and not a replayed saved result.

## Deployment build provenance

The accepted modern Vercel builder contract was verified first on preview deployment `dpl_6Z9G4jaAwCrikcCMAFDefNn9fS3k`, then deployed byte-for-byte to production.

The release bundle contains two files:

1. `vercel_main.py`, which exposes the public FastAPI app and GET acceptance alias;
2. deployment `pyproject.toml`, which pins the exact Git source commit and `strands-agents==1.52.0`, and declares `[tool.vercel] entrypoint = "vercel_main:app"`.

The production build used Vercel CLI 59.11.7, Python 3.12 and uv 0.10.11, installed dependencies from the deployment `pyproject.toml`, compiled Python bytecode, and completed successfully before the canonical alias was observed on the READY deployment.

The previously accepted production deployment `dpl_8b5jXwdhD57u2b4XfvWNRJSLsrey` remains preserved as a rollback candidate.

## Truth boundary

This production evidence proves the current human-first banking judge surface, authentic Strands SDK orchestration/tool execution, external-human-only authority mutation, development-only BANK-ECP evidence invalidation, selective rollback, preservation of unrelated safe work, and blocking/invalidation of the irreversible payment action under stale authority.

It does **not** claim that the public Vercel request uses a foundation model or AgentCore. Separate historical evidence proves a native Amazon Bedrock / Nova Lite Strands acceptance and an AgentCore Runtime deployment/invocation; their recorded truth states remain unchanged. See `bedrock-foundation-model-acceptance-2026-09-01.md`, `agentcore-acceptance-2026-08-23.md`, and `foundation-model-boundary.md`.
