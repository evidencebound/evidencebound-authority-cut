# Authority Cut - Reversible Autonomy with Strands Agents

**One-line pitch:** A professional agent completes routine work autonomously, exposes only the smallest policy-valid semantic human authorities for protected effects, and propagates later human correction through already-executed reversible descendants without erasing unrelated safe work.

## Submission readiness - READY

Authority Cut is the AWS Agents for Humans / Professional Agents submission candidate.

Verified evidence includes:

- authentic Strands Agents SDK orchestration;
- real model-callable tool execution;
- one deep vendor-onboarding professional workflow;
- policy-bounded semantic Authority Cut computation;
- external-human-only grant/revocation boundary;
- correction propagation through an action DAG;
- reversible compensation;
- separately gated irreversible first-funds action;
- public CI and public live judge surface;
- verified Amazon Bedrock AgentCore Runtime deployment and live invocation;
- **verified native Amazon Bedrock / Amazon Nova Lite foundation-model-backed Strands execution**.

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

## Native Amazon Bedrock foundation-model acceptance - VERIFIED

On 2026-09-01 a separate owner-authenticated AWS CloudShell acceptance executed the exact Authority Cut source commit:

`9998565c6db8083446caef7e20a6cf03601533e6`

Target:

- provider: native Amazon Bedrock;
- region: `eu-central-1`;
- inference profile: `eu.amazon.nova-lite-v1:0`;
- profile state: `ACTIVE`, `SYSTEM_DEFINED`, 4 target models;
- Strands version: `1.52.0`;
- same three model-callable tools;
- `authority_mutation_tools=[]`;
- authority mutation remained external-human-only.

Independent direct runtime probe:

```text
DIRECT_CONVERSE=PASS
STOP_REASON=end_turn
INPUT_TOKENS=8
OUTPUT_TOKENS=5
TOTAL_TOKENS=13
```

Full Strands / Authority Cut acceptance:

```text
AUTHORITY_CUT_BEDROCK=PASS
EXECUTION=REAL_STRANDS_AGENT_LOOP_FOUNDATION_MODEL
FOUNDATION_MODEL_INVOCATION=PASS
```

The fail-closed promotion gate requires three distinct model response SHA-256 receipts with positive token usage and all existing control/correction invariants before it can return PASS.

This does **not** change the public Vercel proof into a paid-model route and does **not** retroactively make the historical AgentCore invocation foundation-model-backed.

See `docs/bedrock-foundation-model-acceptance-2026-09-01.md`.

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

That historical AgentCore Runtime used the deterministic custom Strands provider. Its recorded foundation-model status remains historically correct. The later native Bedrock acceptance is a distinct execution path.

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

The public demo intentionally creates no external vendor or payment effects and intentionally remains credential-free.

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

Native Bedrock acceptance, with an authenticated AWS identity:

```bash
python -m pip install -e '.[aws]'
python scripts/run_bedrock_acceptance.py \
  --region eu-central-1 \
  --model-id eu.amazon.nova-lite-v1:0 \
  --output /tmp/authority-cut-bedrock-acceptance.json
```

AgentCore source contract:

```bash
python -m pip install -e '.[agentcore,dev]'
python scripts/run_agentcore_contract_probe.py
```

## Foundation-model boundary

Current truth boundary:

- native Amazon Bedrock / Amazon Nova Lite real model invocation: **PASS**;
- full native Bedrock Strands Authority Cut acceptance: **PASS**;
- historical optional Vercel AI Gateway adapter contract: **PASS**;
- historical Vercel AI Gateway model request: **UNRUN**;
- canonical public Vercel proof: deterministic custom Strands provider;
- historical AgentCore invocation: deterministic custom Strands provider.

See `docs/foundation-model-boundary.md`.

## Historical AWS identity boundary

An earlier non-mutating GitHub OIDC probe could not reuse a pre-existing EvidenceBound deployment role from the new competition repository identity. That specific path remains `BLOCKED_AWS_OIDC_TRUST`.

Verified AWS acceptances used independently authenticated AWS CloudShell paths; no need arose to weaken the historical OIDC trust boundary.

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
- `docs/bedrock-foundation-model-acceptance-2026-09-01.md`
- `docs/agentcore-acceptance-2026-08-23.md`
- `docs/foundation-model-boundary.md`
- `docs/aws-capability-boundary.md`
- `handoff/AWS_JUDGE_PACK.md`
- `handoff/BEDROCK_FOUNDATION_MODEL_ADDENDUM.md`
- `handoff/DEVPOST_FINAL_CHECKLIST.md`
- `qa/QA_RECEIPT.json`
