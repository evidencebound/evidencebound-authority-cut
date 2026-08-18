# AWS Agents for Humans — Submission Handoff

## Identity

**Canonical project name:** Authority Cut

**One-line pitch:** A Strands professional agent completes routine work autonomously, exposes only the minimum policy-valid semantic human authorities for protected effects, and propagates later human correction through reversible downstream execution.

**Invention definition:** Authority Cut Sets + Reversible Correction Propagation.

## What is genuinely implemented and verified

- dedicated public competition repository created during the submission period;
- new competition-period vendor-onboarding action DAG;
- 5 safe + 7 protected effects;
- 3 policy-defined semantic decision bundles;
- exact minimum cover over those bundles;
- prerequisite/receipt-bound human decisions;
- external-human-only approve/revoke boundary;
- model tool set without approve/revoke capabilities;
- correction propagation, descendant invalidation and compensation;
- local SQLite reference effects;
- truthful local judge UI/API;
- deterministic tests and compile gates;
- public GitHub Actions matrix PASS;
- current `strands-agents` installed in public CI and `build_agent()` successfully constructed an actual Strands `Agent` with the three non-authorizing model tools.

## What is not yet verified

- a real Strands-supported model invoking the three tools through the full judge workflow;
- AgentCore deployment;
- public AWS judge endpoint;
- authenticated principal identity;
- real enterprise vendor-system integrations.

## Controlled proof

Observed fixed-workflow metrics:
- protected effects: 7;
- policy-defined Authority Cut decisions: 3;
- per-effect baseline prompts: 7;
- controlled prompt reduction: 57.14%;
- safe actions before human attention: 5;
- reversible protected effects rolled back after correction: 6;
- irreversible effects executed without `funds_release`: 0.

Do not generalize these numbers beyond the controlled workflow.

## Public Strands/CI evidence

- GitHub Actions run: `32179743430`;
- tested branch head: `e297a0600ca2ccfbdff1eec3fbf9309e71eff37c`;
- overall conclusion: `success`;
- deterministic Python 3.11/3.12/3.13 lanes: PASS;
- Strands lane: PASS — installed `.[aws,dev]`, imported the real SDK, and constructed `build_agent()`;
- tool-boundary assertion: PASS — the published model-callable set contains no approve/revoke authority mutation tool.

This proves SDK compatibility and Agent construction. It does **not** prove a foundation model has executed the full workflow.

## Judge sequence after remaining external blockers are removed

1. Open public UI; verify Strands/AgentCore status is truthful.
2. Run safe work: five actions execute, activation remains blocked.
3. Inspect Authority Cut: vendor-risk is ready; later decisions remain future/not-ready.
4. Through **external human UI**, approve vendor-risk.
5. Let the real Strands agent resume already-authorized work.
6. Approve payment-release externally; remittance preview executes; transmit remains blocked.
7. Show first-funds is now ready but still a distinct irreversible authority.
8. Revoke vendor-risk externally.
9. Show six reversible protected descendants rolled back and transmit invalidated while safe work remains.
10. Show the Strands tool list/trace contains no authority mutation tool.

## Pre-existing-work disclosure

Pre-existing EvidenceBound concepts include provenance/evidence binding, dependency graphs, fail-closed verification, selective invalidation/recovery and proof receipts. No source file from EvidenceBound Core, Recovery Mesh, Verified Memory, DataHub Gate or SignalReview is copied into this project. See `docs/preexisting-work.md`.

The public repository preserves its original GitHub initial commit as the parent of the competition source publication, rather than rewriting history. See `docs/repository-provenance.md`.

## Remaining blockers / owner-enabled environment actions

### 1. Real Strands model invocation — BLOCKED
Public CI proves the SDK installs and the Agent constructs. The next acceptance gate is a real Strands-supported model executing the end-to-end workflow through exactly the three non-authorizing tools, including adversarial attempts to self-approve or bypass authority.

### 2. AgentCore — UNVERIFIED / BLOCKED
After the real Strands path passes, deploy to AgentCore only if Runtime/Identity/Observability materially strengthens Technical Implementation without weakening the external-human authority boundary.

### 3. Public judge deployment — BLOCKED
Deploy the exact accepted source to an externally reachable endpoint and run the full judge smoke path. Do not convert this state to PASS until the live endpoint is observed.

## Capture targets

- hero state showing `MODEL CANNOT APPROVE ITSELF`;
- 5 safe actions executed, protected effects blocked;
- 3-bundle Authority Cut with readiness states;
- premature first-funds rejection;
- external human approvals;
- remittance receipt enabling first-funds readiness;
- correction receipt + six rollbacks;
- Strands tool list / trace proving no approve/revoke tool;
- AgentCore trace only after verified live deployment.

## Strongest safe claims

- “The model cannot approve itself through the published Strands tool set.”
- “Public GitHub Actions installed the real Strands SDK and successfully constructed the three-tool Agent.”
- “In the fixed vendor-onboarding workflow, seven protected effects are governed by three policy-defined semantic authorities.”
- “A later human revocation propagates through already-executed reversible descendants in the controlled path.”

Avoid “first”, “unique”, “solves agent safety”, or general productivity claims.
