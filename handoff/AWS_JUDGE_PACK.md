# AWS Agents for Humans — Submission Handoff

## Identity

**Canonical project name:** Authority Cut

**One-line pitch:** A Strands professional agent completes routine work autonomously, exposes only the minimum policy-valid semantic human authorities for protected effects, and propagates later human correction through reversible downstream execution.

**Invention definition:** Authority Cut Sets + Reversible Correction Propagation.

## What is genuinely implemented

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
- tests, CI configuration, threat model and pre-existing-work disclosure.

## What is not yet verified

- real Strands SDK/model execution;
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

## Judge sequence after external blockers are removed

1. Open public UI; verify Strands/AgentCore status is truthful.
2. Run safe work: five actions execute, activation remains blocked.
3. Inspect Authority Cut: vendor-risk is ready; later decisions remain future/not-ready.
4. Through **external human UI**, approve vendor-risk.
5. Let Strands resume already-authorized work.
6. Approve payment-release externally; remittance preview executes; transmit remains blocked.
7. Show first-funds is now ready but still a distinct irreversible authority.
8. Revoke vendor-risk externally.
9. Show six reversible protected descendants rolled back and transmit invalidated while safe work remains.
10. Show model tool list contains no authority mutation tool.

## Pre-existing-work disclosure

Pre-existing EvidenceBound concepts include provenance/evidence binding, dependency graphs, fail-closed verification, selective invalidation/recovery and proof receipts. No source file from EvidenceBound Core, Recovery Mesh, Verified Memory, DataHub Gate or SignalReview is copied into this project. See `docs/preexisting-work.md`.

## Exact external blockers / owner actions

### 1. New GitHub repository — BLOCKED
Current connector cannot create repositories and no distinct unused competition repo exists.

Owner action: create a new public repository dedicated to Authority Cut after 2026-08-10, with no template carrying non-standard project code. Then push this local source tree as its initial history.

### 2. Strands runtime — BLOCKED in current environment
Current container has no `strands-agents` package and cannot reach package indexes.

Owner/unblocked-environment action: allow networked CI or development environment to run `python -m pip install -e '.[aws,dev]'`, instantiate `build_agent()`, then execute the judge workflow with a real Strands-supported model.

### 3. AgentCore — UNVERIFIED
After Strands acceptance, deploy to AgentCore only if Runtime/Identity/Observability can be added without weakening the external human authority boundary. Preserve a non-AgentCore rollback path until live acceptance passes.

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
- “In the fixed vendor-onboarding workflow, seven protected effects are governed by three policy-defined semantic authorities.”
- “A later human revocation propagates through already-executed reversible descendants in the controlled path.”

Avoid “first”, “unique”, “solves agent safety”, or general productivity claims.
