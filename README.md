# Authority Cut — Human-controlled vendor onboarding for bank AI agents

**A bank lets an AI onboard a vendor. The AI does the routine work. A human approves the risky decision. If the evidence changes, affected work is undone and payment stays blocked.**

Authority Cut is a working Strands agent for bank third-party risk, vendor-risk, compliance, procurement, and operational-risk teams. It handles routine onboarding work autonomously, but decisions with real compliance or financial consequences stay with a human. A narrow **BANK-ECP** evidence gate makes the regulatory evidence load-bearing: when the evidence supports the vendor-risk premise, the decision can be presented to the reviewer; when that evidence later changes from `PASS` to `HOLD`, the old approval becomes stale.

The visible result is the product: protected vendor setup that depended on the stale approval is undone, unrelated routine work remains intact, and the irreversible first payment cannot proceed.

## What a judge sees

1. The AI completes five routine vendor-onboarding actions without interrupting the bank employee.
2. BANK-ECP-style evidence evaluation returns `PASS`, and the human receives the vendor-risk decision.
3. The human approves; vendor activation, ERP/purchasing setup, and payment-profile preparation proceed.
4. The evidence is corrected and the gate becomes `HOLD`.
5. Six affected reversible protected actions are rolled back, five unrelated safe actions remain executed, and first funds stays blocked from execution.

Public judge URL:

`https://evidencebound-authority-cut.vercel.app`

Public repository:

`https://github.com/evidencebound/evidencebound-authority-cut`

## Why this matters

Approval workflows usually answer a point-in-time question: *did a person approve this?* Autonomous agents create a harder problem: *does that approval still authorize work after the evidence underneath it changes?*

Authority Cut makes a human correction operational instead of merely conversational. The system can invalidate stale authority, unwind only the affected reversible work, preserve unrelated valid work, and keep an irreversible financial action from executing under stale approval.

The public banking workflow is synthetic and safe for judging; it does not create external vendor records or move real funds.

## BANK-ECP → Authority Cut

The public integration is intentionally narrow rather than embedding the private BANK-ECP benchmark runtime.

```text
Authoritative regulatory evidence
        ↓
Sanitized BANK-ECP evidence gate
        ↓
PASS / HOLD + reasons
        ↓
Human vendor-risk decision
        ↓
Strands agent executes only recorded authority
        ↓
Evidence changes: PASS → HOLD
        ↓
Stale authority invalidated
        ↓
Affected reversible work undone
Safe work preserved
First payment blocked from execution
```

The public bridge uses a development-only DORA third-party-risk fixture with source locator **Regulation (EU) 2022/2554, Article 28(1)(a)**. It is explicitly `DEVELOPMENT_ONLY` and `NOT_FORMAL_BENCHMARK_EVIDENCE`; **no model-performance result is claimed**. See `docs/bank-ecp-bridge.md`.

Model confidence never creates human authority.

## Real Strands execution

The public judge path executes a real Strands SDK `Agent` loop. The model-callable tools remain exactly:

1. `execute_safe_vendor_work`
2. `get_authority_cut`
3. `execute_authorized_vendor_work`

There is no approve or revoke tool in the published Strands tool schema. Evidence correction is also not a model-callable authority-mutation tool. Human grant/revocation remains an external principal action recorded in the shared `ControlPlane`.

The credential-free public proof uses a deterministic custom Strands `Model` provider so a judge can reproduce the complete tool loop without AWS credentials. Its current product sequence is:

```text
routine vendor work + evidence PASS
→ external human vendor-risk approval
→ protected vendor setup
→ external human payment-profile approval
→ first-funds decision becomes ready but transmit remains blocked
→ evidence changes PASS → HOLD
→ stale vendor-risk authority invalidated
→ 6 affected reversible protected effects ROLLED_BACK
→ 5 unrelated safe actions remain EXECUTED
→ irreversible transmit INVALIDATED / cannot execute under stale authority
```

The public route intentionally does **not** claim a foundation-model or AgentCore invocation for that request.

## Technical mechanism

Under the human-facing product is the original Authority Cut mechanism. Protected effects declare policy requirements, policy defines valid **semantic authority** bundles, prerequisite receipts determine when a human decision is ready, and the control plane computes the currently actionable authority cut. A later human revocation or evidence invalidation propagates through the action graph and compensates reversible descendants without erasing unrelated safe work.

The historical controlled workflow remains available as a separate evaluation surface:

```text
7 protected effects
→ 3 semantic human authorities
→ 6 reversible descendants rolled back after correction
→ 5 unrelated safe actions preserved
→ irreversible transmit INVALIDATED
```

That controlled `7 → 3` result is not presented as measured customer productivity.

## Native Amazon Bedrock foundation-model acceptance — VERIFIED

On **2026-09-01**, a separate owner-authenticated AWS CloudShell acceptance executed exact Authority Cut source commit:

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

The fail-closed promotion gate requires three distinct model-response SHA-256 receipts with positive token usage and all existing control/correction invariants before it can return PASS.

This historical acceptance does **not** turn the public Vercel proof into a paid-model route and does **not** retroactively make the historical AgentCore invocation foundation-model-backed.

See `docs/bedrock-foundation-model-acceptance-2026-09-01.md`.

## Amazon Bedrock AgentCore Runtime — VERIFIED

On **2026-08-23**, Authority Cut was deployed to Amazon Bedrock AgentCore Runtime and invoked through the real AgentCore data plane.

Accepted configuration:

- region: `eu-central-1` (Frankfurt);
- Runtime name: `AuthorityCutRuntime`;
- Runtime version: `1`;
- status: `READY`;
- direct-code S3 CodeZip;
- runtime: `PYTHON_3_13`;
- entry point: `agentcore_main.py`;
- network mode: `PUBLIC`;
- packaged source HEAD: `200d71f963bb4496a6f01a6cf1788695b3164739`;
- CodeZip SHA-256: `67c9ce7de97f48970d3c595e6914fef314011fa5cebccf4f01cd4b6bea32690e`.

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

That historical AgentCore Runtime used the deterministic custom Strands provider. Its recorded foundation-model status remains historically correct. The later 2026-09-01 native Bedrock acceptance is a distinct execution path.

See `docs/agentcore-acceptance-2026-08-23.md`.

## Controlled evaluation boundary

The original fixed vendor-onboarding workflow records:

- safe actions before human attention: **5**;
- protected effects: **7**;
- one-approval-per-protected-effect baseline: **7** decisions;
- semantic Authority Cut decisions: **3**;
- decision reduction in that fixed workflow: **57.14%**;
- executed reversible protected effects before correction: **6**;
- reversible protected effects rolled back after correction: **6/6**;
- irreversible effects executed without `funds_release`: **0**;
- unrelated safe actions preserved: **5**.

The 57.14% value is scoped only to this controlled workflow. No generalized customer productivity, ROI, adoption, or field-study claim is made.

## Public judge path

Open:

`https://evidencebound-authority-cut.vercel.app`

Select **Run the end-to-end banking scenario**.

The service executes a reset-each-call synthetic vendor-onboarding workflow and returns the real execution ledger; it is not a saved replay. Machine-readable surfaces include:

- `/health`
- `/api/tool-boundary`
- `/api/evaluation`
- `POST /api/strands-proof`
- `/api/strands-proof-get`

The public demo intentionally creates no external vendor or payment effects and remains credential-free.

## Reproduce locally

Deterministic kernel:

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

This dedicated repository and its vendor-onboarding graph, Authority Cut mechanism, Strands orchestration, evaluation, AgentCore adapter, and judge surface were authored during the competition period.

Pre-existing EvidenceBound concepts disclosed for completeness include provenance/evidence binding, dependency graphs, fail-closed verification, selective invalidation/recovery, and proof receipts.

The BANK-ECP bridge added for the banking product is a sanitized public integration artifact. It does not copy the private benchmark runtime or expose sealed-holdout/private benchmark construction artifacts.

No source file from EvidenceBound Core, Recovery Mesh, Verified Memory, DataHub Gate, or SignalReview was copied into this project.

See `docs/preexisting-work.md`, `docs/repository-provenance.md`, and `docs/bank-ecp-bridge.md`.

## Limitations

Authority Cut does not prove:

- correctness of arbitrary enterprise policy;
- legal authorization or regulatory compliance certification;
- correctness of every regulatory interpretation;
- authenticated end-user principal identity;
- safe compensation in arbitrary external systems;
- durable distributed authority state;
- general corrigibility, alignment, or autonomous-agent safety;
- generalized productivity improvement;
- BANK-ECP model superiority or formal holdout performance.

Minimality is exact only over the policy-defined semantic decision bundles supplied to the runtime. The public banking workflow uses synthetic in-memory/reference effects for safe judging.

## Evidence pack

- `docs/bank-ecp-bridge.md`
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
