# AWS Agents for Humans — Authority Cut Judge Pack

Snapshot updated: 2026-09-07

## Current sprint status

**BANKING PRODUCT REFRESH IS ON FEATURE BRANCH; PRODUCTION/DEVPOST REMAIN ON THE PRIOR SUBMITTED VERSION UNTIL FINAL VERIFICATION.**

Do not describe the refreshed banking surface as production until the release commit is merged, deployed, browser-smoked, and read back from production.

## The product in one sentence

> A bank lets an AI onboard a vendor. The AI does the routine work. A human approves the risky decision. If the evidence changes, affected work is undone and payment stays blocked.

**Primary user:** bank third-party risk, vendor-risk, compliance, procurement, and operational-risk professionals.

**Track:** Professional Agents.

Public repository:

`https://github.com/evidencebound/evidencebound-authority-cut`

Current production judge URL:

`https://evidencebound-authority-cut.vercel.app`

Devpost:

`https://devpost.com/software/authority-cut`

Current submitted video:

`https://youtu.be/dY8W-AP4mms`

The video has not been replaced during the banking refresh. Replace it only if the new product story materially improves Presentation and the replacement can be fully reverified before the deadline.

## What the refreshed judge path demonstrates

1. **AI routine work** — the Strands agent completes five safe vendor-onboarding actions.
2. **Evidence check** — a sanitized BANK-ECP DORA bridge returns `PASS` for the vendor-responsibility premise.
3. **Human risky decision** — the external bank reviewer approves `vendor-risk`.
4. **Protected work** — vendor activation, ERP/purchasing setup, and later payment-profile preparation proceed under recorded human authority.
5. **Irreversible boundary** — first funds remains separately gated and does not execute.
6. **Evidence changes** — the BANK-ECP bridge changes from `PASS` to `HOLD` with `MATERIAL_CITATION_MISMATCH`.
7. **Operational correction** — the stale vendor-risk authority is invalidated; six affected reversible protected effects are rolled back, five unrelated safe actions remain executed, and first payment remains unable to execute.

The key change from the older demo is that the public magic moment is now **evidence-driven**. Human revocation remains supported as a separate external-principal correction path, but it is not the flagship trigger.

## BANK-ECP boundary

The public bridge is deliberately narrow. It does not embed the private BANK-ECP benchmark runtime or expose formal holdout artifacts.

Public source locator:

`Regulation (EU) 2022/2554, Article 28(1)(a)`

Public bridge classification:

```text
DEVELOPMENT_ONLY
NOT_FORMAL_BENCHMARK_EVIDENCE
```

No model-performance result is claimed. Model confidence never creates authority.

See `docs/bank-ecp-bridge.md`.

## What judges can verify in the public Strands proof

The refreshed feature-branch proof executes a real Strands SDK Agent/tool loop with a deterministic custom Model provider and a reset-each-call synthetic vendor workflow. It is not a saved replay.

Expected accepted result after release:

```text
execution = REAL_STRANDS_AGENT_LOOP_DETERMINISTIC_MODEL
model_provider = deterministic-public-proof
strands_tools = [
  execute_safe_vendor_work,
  get_authority_cut,
  execute_authorized_vendor_work
]
authority_mutation_tools = []
authority_boundary = EXTERNAL_HUMAN_ONLY
correction_trigger = BANK_ECP_EVIDENCE_CHANGE
bank_ecp_evidence_before_correction.verdict = PASS
bank_ecp_evidence_after_correction.verdict = HOLD
safe_actions_preserved = 5
protected_reversible_effects_rolled_back = 6
irreversible_transmit_after_correction = INVALIDATED
```

The public route intentionally remains deterministic and credential-free. `INVALIDATED` is the execution-state term for the pending irreversible transmit after stale authority is removed; human-facing copy says payment stays blocked from execution.

## Authority boundary

The model-callable Strands tool set is exactly:

1. `execute_safe_vendor_work`
2. `get_authority_cut`
3. `execute_authorized_vendor_work`

There is no approve, revoke, evidence-correction, or authority-restoration tool. Human grant/revocation remains external. Evidence updates also arrive through a non-model channel.

## Native Amazon Bedrock / Nova Lite — VERIFIED HISTORICAL ACCEPTANCE

Accepted 2026-09-01 through owner-authenticated AWS CloudShell at exact source:

`9998565c6db8083446caef7e20a6cf03601533e6`

Configuration/readback:

- region: `eu-central-1`;
- inference profile: `eu.amazon.nova-lite-v1:0`;
- status: `ACTIVE`;
- type: `SYSTEM_DEFINED`;
- target model count: 4;
- native Strands `BedrockModel`;
- same exact three non-authorizing model tools;
- human grant/revocation outside the model tool surface.

Independent direct runtime probe:

```text
DIRECT_CONVERSE=PASS
STOP_REASON=end_turn
INPUT_TOKENS=8
OUTPUT_TOKENS=5
TOTAL_TOKENS=13
```

Full Strands Authority Cut result:

```text
AUTHORITY_CUT_BEDROCK=PASS
EXECUTION=REAL_STRANDS_AGENT_LOOP_FOUNDATION_MODEL
FOUNDATION_MODEL_INVOCATION=PASS
```

The fail-closed promotion gate requires three distinct model-response SHA-256 receipts with positive token usage and all control/correction invariants before PASS can be returned.

This acceptance is a separate historical execution path. It does not make the refreshed public Vercel request foundation-model-backed.

See:

- `docs/bedrock-foundation-model-acceptance-2026-09-01.md`
- `handoff/BEDROCK_FOUNDATION_MODEL_ADDENDUM.md`

## Amazon Bedrock AgentCore — VERIFIED HISTORICAL ACCEPTANCE

Accepted 2026-08-23 through owner-authenticated AWS CloudShell.

Configuration:

- region: `eu-central-1`;
- Runtime: `AuthorityCutRuntime`, version `1`;
- status: `READY`;
- direct-code / S3 CodeZip;
- runtime: `PYTHON_3_13`;
- entry point: `agentcore_main.py`;
- network mode: `PUBLIC`;
- packaged source HEAD: `200d71f963bb4496a6f01a6cf1788695b3164739`;
- CodeZip SHA-256: `67c9ce7de97f48970d3c595e6914fef314011fa5cebccf4f01cd4b6bea32690e`.

A real `InvokeAgentRuntime` call returned HTTP 200 and passed the Strands loop and authority/correction assertions.

Historical result:

```text
AGENTCORE_RUNTIME_DEPLOYMENT=PASS
AGENTCORE_LIVE_INVOCATION=PASS
STRANDS_LOOP_INSIDE_AGENTCORE=PASS
HUMAN_AUTHORITY_BOUNDARY=PASS
SAFE_ACTIONS_PRESERVED=5
REVERSIBLE_EFFECTS_ROLLED_BACK=6
IRREVERSIBLE_TRANSMIT=INVALIDATED
FOUNDATION_MODEL_INVOCATION=UNVERIFIED
```

Important historical boundary: that AgentCore Runtime used the deterministic custom Strands provider. Its recorded `FOUNDATION_MODEL_INVOCATION=UNVERIFIED` remains correct. The 2026-09-01 native Bedrock acceptance is a distinct execution path.

## Original controlled evaluation

The historical fixed workflow remains preserved rather than retroactively rewritten by BANK-ECP integration:

- safe actions before human intervention: **5**;
- protected effects: **7**;
- one-approval-per-protected-effect baseline decisions: **7**;
- semantic Authority Cut decisions: **3**;
- decision reduction versus that fixed baseline: **57.14%**;
- reversible protected effects executed before correction: **6**;
- reversible protected effects rolled back after correction: **6/6**;
- irreversible effects executed without `funds_release`: **0**;
- unaffected safe actions preserved: **5**.

Do not generalize 57.14% into measured customer productivity, ROI, or adoption.

## Rubric mapping

### Technological Implementation

Lead evidence:

- authentic Strands Agent/tool orchestration;
- exact restricted model-callable tool boundary;
- real public execution path;
- load-bearing BANK-ECP evidence gate;
- execution-time authority validity;
- selective compensation and preserved safe work;
- separate irreversible first-funds authority;
- verified historical native Bedrock / Nova Lite foundation-model execution;
- verified historical AgentCore Runtime deployment and invocation;
- public CI and exact-source snapshots.

### Design

Lead with the banking product, not the control-plane vocabulary:

- AI handles routine vendor onboarding;
- human sees the risky decision;
- evidence can change after approval;
- affected work is visibly undone;
- unrelated safe work remains;
- payment stays blocked.

Technical diagnostics are below the product story.

### Potential Impact

Target audience is specific: banks and regulated financial institutions deploying agents into third-party risk, vendor management, compliance, procurement, and financial operations.

Commercial hypothesis: organizations need human authority to remain effective after autonomous work has started and after evidence changes. Customer adoption, measured ROI, and productivity gains remain unverified.

### Creativity & Originality

The strongest competition contribution is the concrete composition of:

- evidence-gated human authority;
- authority mutation kept outside the model tool surface;
- policy-defined semantic authority bundles;
- execution-time revalidation; and
- selective correction of already-executed reversible descendants while unrelated work survives and irreversible payment remains blocked.

Do not claim invention of HITL, interrupt/resume, revocable authorization, provenance, dependency invalidation, or compensation generally.

### Presentation

Demo order:

```text
bank employee problem
→ AI routine work
→ BANK-ECP evidence PASS
→ human risky decision
→ protected work
→ evidence PASS → HOLD
→ affected work undone
→ safe work preserved
→ payment blocked
→ only then Strands / Bedrock / AgentCore / architecture
```

## Prior-art boundary

Safe novelty language:

> Authority Cut keeps consequential authority outside the model, binds it to current evidence, and makes later evidence or human corrections change already-started execution rather than merely changing an audit record.

No `first`, `unique`, `only`, patentability, alignment-solved, or universal-safety claim.

## Pre-existing-work disclosure

Pre-existing EvidenceBound concepts include provenance/evidence binding, dependency graphs, fail-closed verification, selective invalidation/recovery, and proof receipts.

This AWS competition repository was created during the submission period. Its vendor-onboarding graph, Authority Cut mechanism, Strands orchestration, evaluation, AgentCore adapter, and public judge service are competition-period work.

The BANK-ECP public bridge is a sanitized integration artifact. It does not copy the private BANK-ECP runtime or sealed/private benchmark artifacts into this repository.

No source file from EvidenceBound Core, Recovery Mesh, Verified Memory, DataHub Gate, or SignalReview was copied into this project.

## Provider and identity boundaries

- native Amazon Bedrock / Nova Lite foundation-model acceptance: **PASS**;
- historical AgentCore Runtime deployment/invocation: **PASS**;
- historical AgentCore foundation-model invocation: **UNVERIFIED**;
- historical optional Vercel AI Gateway provider contract: **PASS**;
- historical Vercel AI Gateway model invocation: **UNRUN**;
- historical reuse of a pre-existing EvidenceBound GitHub OIDC role: `BLOCKED_AWS_OIDC_TRUST`;
- public Vercel request: deterministic Strands provider, not Bedrock/AgentCore.

Do not rewrite historical failed, blocked, unrun, or unverified paths as PASS.

## Release gate before calling the banking refresh complete

The feature branch is not the external acceptance condition. Completion requires:

1. full CI success on the exact release commit;
2. reviewed diff with no private BANK-ECP leakage or unsupported claims;
3. merge to `main`;
4. Vercel production deployment readback;
5. browser smoke of the 5-second and 60-second banking story;
6. README/production consistency;
7. Devpost human-first rewrite and authenticated submitted-state readback;
8. video decision based on Presentation ROI;
9. any new thumbnail / YouTube / Devpost visual created strictly through Google Slides;
10. final freeze.

## Verified limitations

- real customer productivity/adoption: **UNVERIFIED**;
- arbitrary external-system compensation safety: **UNVERIFIED**;
- formal BANK-ECP model-performance result: **NOT CLAIMED**;
- regulatory certification/legal advice: **NOT CLAIMED**;
- general corrigibility/alignment claim: **NOT CLAIMED**.
