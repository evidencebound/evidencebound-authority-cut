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
- current `strands-agents` installed in public CI;
- `build_agent()` constructed a real Strands `Agent`;
- the real Strands Agent loop executed all three published tools using a deterministic custom Strands `Model` provider while authority mutations remained external to the model tool set.

## What is not yet verified

- foundation-model execution of the full workflow (for example Bedrock-backed Strands);
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

Strongest current public run:
- GitHub Actions run: `32180475314`;
- tested branch head: `27f433ecb12fc57ef087b6aa6bf4df9a78ba1004`;
- overall conclusion: `success`;
- deterministic Python 3.11/3.12/3.13 lanes: PASS;
- `strands-agents` version observed: `1.52.0`;
- Strands runtime job: `95852058241`;
- `build_agent()` construction: PASS;
- real Strands Agent loop/tool execution: PASS;
- published tools observed in the loop: `execute_safe_vendor_work`, `get_authority_cut`, `execute_authorized_vendor_work`;
- safe work and authority-surface inspection: PASS;
- externally granted authorized resume: PASS;
- correction path: PASS — six reversible protected effects rolled back and irreversible transmit became `INVALIDATED`;
- authority mutation tools visible to the model: none.

The CI provider is deliberately deterministic and credential-free. This proves authentic Strands SDK orchestration/tool execution; it does **not** establish foundation-model quality, Bedrock execution, or AgentCore behavior.

## Judge sequence after remaining external blockers are removed

1. Open public UI; verify Strands/AgentCore status is truthful.
2. Run safe work through the Strands agent: five actions execute, activation remains blocked.
3. Inspect Authority Cut: vendor-risk is ready; later decisions remain future/not-ready.
4. Through **external human UI**, approve vendor-risk.
5. Let the foundation-model-backed Strands agent resume already-authorized work.
6. Approve payment-release externally; remittance preview executes; transmit remains blocked.
7. Show first-funds is now ready but still a distinct irreversible authority.
8. Revoke vendor-risk externally.
9. Show six reversible protected descendants rolled back and transmit invalidated while safe work remains.
10. Show the Strands trace/tool list contains no authority mutation tool.

## Pre-existing-work disclosure

Pre-existing EvidenceBound concepts include provenance/evidence binding, dependency graphs, fail-closed verification, selective invalidation/recovery and proof receipts. No source file from EvidenceBound Core, Recovery Mesh, Verified Memory, DataHub Gate or SignalReview is copied into this project. See `docs/preexisting-work.md`.

The public repository preserves its original GitHub initial commit as the parent of the competition source publication, rather than rewriting history. See `docs/repository-provenance.md`.

## Remaining blockers / owner-enabled environment actions

### 1. Foundation-model Strands execution — BLOCKED
The SDK Agent loop is now publicly proven. The remaining model gate is a real Strands-supported foundation model executing the same end-to-end workflow through exactly the three non-authorizing tools, including adversarial attempts to self-approve or bypass authority.

### 2. AgentCore — UNVERIFIED / BLOCKED
After the foundation-model path passes, deploy to AgentCore only if Runtime/Identity/Observability materially strengthens Technical Implementation without weakening the external-human authority boundary.

### 3. Public judge deployment — BLOCKED
Deploy the exact accepted source to an externally reachable endpoint and run the full judge smoke path. Do not convert this state to PASS until the live endpoint is observed.

## Capture targets

- hero state showing `MODEL CANNOT APPROVE ITSELF`;
- public CI trace showing real Strands tool execution;
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
- “Public GitHub Actions installed Strands Agents 1.52.0 and executed the real Strands Agent loop through all three Authority Cut tools.”
- “The public loop proof uses a deterministic custom Strands model provider; foundation-model and AgentCore execution remain separate live gates.”
- “In the fixed vendor-onboarding workflow, seven protected effects are governed by three policy-defined semantic authorities.”
- “A later human revocation propagates through already-executed reversible descendants in the controlled path.”

Avoid “first”, “unique”, “solves agent safety”, or general productivity claims.
