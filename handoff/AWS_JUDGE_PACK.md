# AWS Agents for Humans - Final Submission Handoff

Snapshot updated: 2026-08-23

## Decision

**READY engineering / NOT YET SUBMITTED.**

Authority Cut is the Professional Agents submission candidate. The core public Strands path is independently verifiable, and Amazon Bedrock AgentCore Runtime is now also verified through a real deployment and live invocation.

## Identity

**Project:** Authority Cut

**Track:** Professional Agents

**One-line pitch:** A Strands professional agent completes routine work autonomously, surfaces only the smallest policy-valid semantic human authorities for protected downstream effects, and propagates later human correction through reversible execution without erasing unrelated safe work.

**Competition invention thesis:** **Authority Cut Sets + Reversible Correction Propagation.**

Public repository:

`https://github.com/moneyparking/evidencebound-authority-cut`

Public judge URL:

`https://evidencebound-authority-cut.vercel.app`

## Memorable judge hook

```text
7 protected effects
-> 3 semantic human authorities
-> 6 reversible descendants compensated after correction
-> 5 unrelated safe actions preserved
-> irreversible transmit INVALIDATED
```

## What judges can verify live

Open the public URL and select **Run live Strands judge path**.

The production service executes the real Strands SDK Agent/tool loop against a reset-each-call synthetic vendor-onboarding workflow. It does not replay a saved result.

Accepted live result:

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
safe_actions_preserved = 5
protected_reversible_effects_rolled_back = 6
irreversible_transmit_after_correction = INVALIDATED
receipt_count = 14
```

## Deep professional workflow

### Phase 1 - autonomous safe work

Five routine actions execute before human attention:

1. collect vendor packet;
2. tax check;
3. bank check;
4. draft vendor record;
5. follow-up preparation.

Protected activation remains blocked. `vendor-risk` is ready; later authorities are not ready.

### Phase 2 - vendor-risk authority

An external human principal grants `vendor-risk`. The Strands agent resumes activation, ERP sync and purchasing. Payment work remains blocked until `payment-release` becomes ready.

### Phase 3 - payment-release authority

The external principal grants `payment-release`. Payment-profile, terms and remittance-preview work executes. The remittance receipt makes `first-funds` ready. Irreversible transmit remains blocked because `first-funds` is a distinct authority.

### Phase 4 - correction propagation

The principal revokes the earlier `vendor-risk` authority.

Observed state:

- 6 reversible protected effects -> `ROLLED_BACK`;
- pending irreversible transmit -> `INVALIDATED`;
- 5 unrelated safe actions -> remain `EXECUTED`.

The correction changes downstream execution state rather than merely recording an audit event.

## Authority boundary

The model-callable Strands tool set is exactly:

1. `execute_safe_vendor_work`
2. `get_authority_cut`
3. `execute_authorized_vendor_work`

There is no approve/revoke tool. Human grant/revocation remains an external principal action.

## Fixed-workflow evaluation

Verified controlled metrics:

- safe actions before human intervention: **5**;
- protected effects: **7**;
- one-approval-per-protected-effect baseline decisions: **7**;
- semantic Authority Cut decisions: **3**;
- decision reduction versus that fixed baseline: **57.14%**;
- reversible protected effects executed before correction: **6**;
- reversible protected effects rolled back after correction: **6/6**;
- irreversible effects executed without `funds_release`: **0**;
- unaffected safe actions preserved: **5**.

Do not generalize 57.14% into measured customer productivity.

## Amazon Bedrock AgentCore - VERIFIED

Accepted 2026-08-23 through owner-authenticated AWS CloudShell.

Configuration:

- region: `eu-central-1` (Frankfurt)
- Runtime: `AuthorityCutRuntime`, version `1`
- status: `READY`
- direct-code / S3 CodeZip
- runtime: `PYTHON_3_13`
- entry point: `agentcore_main.py`
- network mode: `PUBLIC`
- packaged source HEAD: `200d71f963bb4496a6f01a6cf1788695b3164739`
- CodeZip SHA-256: `67c9ce7de97f48970d3c595e6914fef314011fa5cebccf4f01cd4b6bea32690e`

Real `InvokeAgentRuntime` returned HTTP 200 and passed:

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

The accepted AgentCore Runtime uses the same deterministic custom Strands `Model` provider as the public reproducible proof. Therefore AgentCore infrastructure execution is PASS while foundation-model invocation remains UNVERIFIED.

See `docs/agentcore-acceptance-2026-08-23.md`.

## Historical AWS identity boundary

An earlier non-mutating GitHub OIDC probe attempted to reuse a pre-existing EvidenceBound deployment role from the new competition repository identity and received `Not authorized to perform sts:AssumeRoleWithWebIdentity`.

That specific reuse path remains `BLOCKED_AWS_OIDC_TRUST`. It was not silently converted to PASS.

The successful AgentCore deployment used an independently authenticated CloudShell path and a dedicated least-privilege Runtime role.

## Current judging-criterion mapping

### Technical Implementation

Lead evidence:

- authentic Strands Agent/tool orchestration;
- exact restricted tool boundary;
- real public execution;
- prerequisite/receipt-gated semantic authority;
- downstream correction propagation and compensation;
- separate irreversible authority;
- verified AgentCore Runtime deployment and invocation;
- public CI and source provenance.

### Design

Authority Cut compresses the decision surface instead of interrupting the operator for each protected effect. Future decisions stay not-ready until prerequisite evidence exists. Corrections affect downstream state while unrelated safe work survives.

### Potential Impact

Target professional domains: procurement, vendor onboarding, finance operations, compliance and insurance operations.

Commercial hypothesis: reusable human-control middleware for long-running professional agents. Real adoption/productivity remains unverified.

### Creativity & Originality

The strongest competition contribution is the concrete composition of:

- exact minimum cover over policy-defined semantic authority bundles currently actionable under evidence/prerequisites; and
- correction-driven selective compensation over already-executed descendants.

Do not claim invention of HITL, interrupt/resume, revocable authorization, provenance, dependency invalidation or compensation generally.

### Presentation

The final video should show the real click on **Run live Strands judge path**, the returned live ledger, and a short AgentCore acceptance proof. Do not spend the demo on deployment commands.

## Prior-art boundary

Current Strands already provides HITL interventions, approval interception and interrupt/resume. Agent governance, delegated authority and transactional/compensation patterns also predate this project.

Safe novelty language:

> Authority Cut changes the granularity and lifecycle of human control: compute the smallest currently actionable policy-defined semantic authority surface, keep authority mutation outside the model toolset, and propagate later revocation through already-executed reversible descendants.

No `first`, `unique`, `only`, patentability, alignment-solved or universal-safety claim.

## Pre-existing-work disclosure

Pre-existing EvidenceBound concepts include provenance/evidence binding, dependency graphs, fail-closed verification, selective invalidation/recovery and proof receipts.

This AWS competition repository was created during the submission period. Its vendor-onboarding graph, Authority Cut mechanism, Strands orchestration, evaluation, AgentCore adapter and public judge service are competition-period work. No source file from EvidenceBound Core, Recovery Mesh, Verified Memory, DataHub Gate or SignalReview was copied into this project.

## Foundation-model boundary

Status:

- optional Strands OpenAI-compatible provider contract: **PASS**;
- actual foundation-model invocation: **UNVERIFIED / UNRUN**.

Do not infer foundation-model execution from the deterministic public proof or AgentCore acceptance.

## Competition / compliance essentials

Preserve in final submission:

- Strands architecturally central;
- new project during competition period;
- public source repository;
- README + architecture documentation;
- Apache-2.0 license;
- public demo/testing path;
- public YouTube/Vimeo demo <=5 minutes;
- AWS Builder ID;
- pre-existing-work disclosure;
- Professional Agents track.

## Remaining critical path

1. final video edit: real public Strands run + concise AgentCore proof;
2. publish video **Public** on YouTube/Vimeo;
3. upload architecture diagram to Devpost;
4. final Devpost write/readback;
5. submit;
6. verify live submitted state.

Optional after submission stability: publish up to three technically substantive qualifying `builder.aws` posts if the current rules still award the bonus.

## Final classification

**READY engineering / NOT YET SUBMITTED.**

Verified limitations:

- foundation-model execution: **UNVERIFIED**;
- real customer productivity/adoption: **UNVERIFIED**;
- arbitrary external-system compensation safety: **UNVERIFIED**.
