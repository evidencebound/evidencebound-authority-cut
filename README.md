# Authority Cut - Reversible Autonomy with Strands Agents

**One-line pitch:** A professional agent completes routine work autonomously, exposes only the smallest policy-valid semantic human authorities for protected effects, and propagates later human correction through already-executed reversible descendants without erasing unrelated safe work.

## Submission readiness - READY

Authority Cut is the AWS Agents for Humans / Professional Agents submission candidate.

Verified submission evidence now includes:

- authentic Strands Agents SDK orchestration;
- real model-callable tool execution;
- one deep vendor-onboarding professional workflow;
- policy-bounded semantic Authority Cut computation;
- external-human-only grant/revocation boundary;
- correction propagation through an action DAG;
- reversible compensation;
- separately gated irreversible first-funds action;
- public CI and public live judge surface;
- **verified Amazon Bedrock AgentCore Runtime deployment and live invocation**.

Public judge URL:

`https://evidencebound-authority-cut.vercel.app`

Public repository:

`https://github.com/evidencebound/evidencebound-authority-cut`

## Competition contribution

Authority Cut does **not** claim to invent HITL, approval workflows, interrupt/resume, revocable grants, dependency invalidation or compensation generally.

The competition thesis is narrower:

1. protected workflow effects declare semantic authority atoms;
2. policy defines valid semantic decision bundles;
3. the control plane computes the smallest currently actionable policy-valid bundle cover;
4. prerequisite receipts determine when a decision is actually ready;
5. human authority remains outside the model-callable Strands tool surface;
6. later revocation propagates through downstream execution;
7. already-executed reversible descendants are compensated while unrelated safe work is preserved;
8. a pending irreversible descendant is invalidated rather than falsely described as rolled back.

Observable fixed-workflow hook:

```text
7 protected effects
-> 3 semantic human authorities
-> 6 reversible descendants compensated after correction
-> 5 unrelated safe actions preserved
-> irreversible transmit INVALIDATED
```

## Real Strands execution

The model-callable Strands tools are exactly:

1. `execute_safe_vendor_work`
2. `get_authority_cut`
3. `execute_authorized_vendor_work`

Approve and revoke are deliberately absent from the published model tool schema.

The canonical public proof executes a real Strands `Agent` loop with a deterministic custom Strands `Model` provider so the judge path is reproducible and credential-free.

Accepted public proof:

```text
execution = REAL_STRANDS_AGENT_LOOP_DETERMINISTIC_MODEL
authority_mutation_tools = []
authority_boundary = EXTERNAL_HUMAN_ONLY
safe_actions_preserved = 5
protected_reversible_effects_rolled_back = 6
irreversible_transmit_after_correction = INVALIDATED
receipt_count = 14
```

## AgentCore Runtime - VERIFIED

On 2026-08-23 Authority Cut was deployed to Amazon Bedrock AgentCore Runtime and invoked through the real AgentCore data plane.

Accepted configuration:

- region: `eu-central-1` (Frankfurt)
- Runtime name: `AuthorityCutRuntime`
- Runtime version: `1`
- status: `READY`
- direct-code S3 CodeZip
- runtime: `PYTHON_3_13`
- entry point: `agentcore_main.py`
- network mode: `PUBLIC`
- packaged source HEAD: `200d71f963bb4496a6f01a6cf1788695b3164739`
- CodeZip SHA-256: `67c9ce7de97f48970d3c595e6914fef314011fa5cebccf4f01cd4b6bea32690e`

A real `InvokeAgentRuntime` call returned HTTP 200 and passed:

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

The successful AgentCore integration does not change the foundation-model truth boundary. The deployed Runtime uses the same deterministic custom Strands `Model` provider as the reproducible public proof.

See `docs/agentcore-acceptance-2026-08-23.md`.

## Fixed-workflow evaluation

Controlled results:

- safe actions before human attention: **5**;
- protected effects: **7**;
- one-approval-per-protected-effect baseline: **7** decisions;
- Authority Cut semantic decisions: **3**;
- decision reduction in this fixed workflow: **57.14%**;
- executed reversible protected effects before correction: **6**;
- reversible protected effects rolled back after correction: **6/6**;
- irreversible effects executed without `funds_release`: **0**;
- unrelated safe actions preserved: **5**.

The 57.14% result is scoped only to this controlled workflow. No generalized customer productivity claim is made.

## Public judge path

Open:

`https://evidencebound-authority-cut.vercel.app`

Select **Run live Strands judge path**.

The page runs a reset-each-call synthetic vendor-onboarding workflow and displays the real execution ledger. Machine-readable surfaces include:

- `/health`
- `/api/tool-boundary`
- `/api/evaluation`
- `POST /api/strands-proof`
- `/api/strands-proof-get`

The public demo intentionally creates no external vendor or payment effects.

## Reproduce locally

```bash
python -m pip install -e '.[dev]' --no-build-isolation
PYTHONPATH=src pytest
PYTHONPATH=src python scripts/run_demo.py
PYTHONPATH=src python scripts/run_evaluation.py
```

Strands lane:

```bash
python -m pip install -e '.[aws,dev]'
python scripts/run_strands_ci_probe.py
python scripts/run_public_strands_surface_probe.py
```

AgentCore source contract:

```bash
python -m pip install -e '.[agentcore,dev]'
python scripts/run_agentcore_contract_probe.py
```

## Foundation-model boundary

The optional OpenAI-compatible Strands provider contract is implemented and fail-closed without a runtime credential.

Correct status:

- provider integration contract: **PASS**;
- actual foundation-model invocation: **UNVERIFIED / UNRUN**.

Do not infer foundation-model execution from the deterministic Strands proof or AgentCore acceptance.

## Historical AWS identity boundary

An earlier non-mutating GitHub OIDC probe could not reuse a pre-existing EvidenceBound deployment role from the new competition repository identity. That specific path remains `BLOCKED_AWS_OIDC_TRUST`.

The verified AgentCore deployment used an independently authenticated AWS CloudShell path and a dedicated least-privilege Runtime execution role. The successful deployment does not retroactively change the historical OIDC result.

## New-project / pre-existing-work disclosure

This dedicated repository and its vendor-onboarding graph, Authority Cut mechanism, Strands orchestration, evaluation, AgentCore adapter and judge surface were authored during the competition period.

Pre-existing EvidenceBound concepts disclosed for completeness include provenance/evidence binding, dependency graphs, fail-closed verification, selective invalidation/recovery and proof receipts.

No source file from EvidenceBound Core, Recovery Mesh, Verified Memory, DataHub Gate or SignalReview was copied into this project.

See `docs/preexisting-work.md` and `docs/repository-provenance.md`.

## Limitations

Authority Cut does not prove:

- correctness of arbitrary enterprise policy;
- legal authorization;
- authenticated end-user principal identity;
- safe compensation in arbitrary external systems;
- durable distributed authority state;
- general corrigibility, alignment or autonomous-agent safety;
- generalized productivity improvement.

Minimality is exact only over the policy-defined semantic decision bundles supplied to the runtime.

## Evidence pack

- `docs/prior-art.md`
- `docs/claims-ledger.md`
- `docs/agentcore-acceptance-2026-08-23.md`
- `docs/aws-capability-boundary.md`
- `handoff/AWS_JUDGE_PACK.md`
- `handoff/DEVPOST_FINAL_CHECKLIST.md`
- `qa/QA_RECEIPT.json`
