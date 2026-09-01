# AWS Agents for Humans - Final Submission Handoff

Snapshot updated: 2026-09-01

## Decision

**READY / SUBMITTED / LIVE READBACK PASS.**

Authority Cut is the Professional Agents submission candidate. The public deterministic Strands judge path is independently verifiable, Amazon Bedrock AgentCore Runtime deployment/invocation is verified, a separate native Amazon Bedrock / Amazon Nova Lite foundation-model-backed Strands acceptance is verified, and the authenticated Devpost project was read back after the evidence update with its submitted relationship intact.

## Identity

**Project:** Authority Cut

**Track:** Professional Agents

**One-line pitch:** A Strands professional agent completes routine work autonomously, surfaces only the smallest policy-valid semantic human authorities for protected downstream effects, and propagates later human correction through reversible execution without erasing unrelated safe work.

**Competition invention thesis:** **Authority Cut Sets + Reversible Correction Propagation.**

Public repository:

`https://github.com/evidencebound/evidencebound-authority-cut`

Public judge URL:

`https://evidencebound-authority-cut.vercel.app`

Devpost:

`https://devpost.com/software/authority-cut`

Video:

`https://youtu.be/dY8W-AP4mms`

Do not replace the video solely for the later Bedrock acceptance.

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

Accepted public live result:

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

The public route intentionally stays deterministic and credential-free.

## Native Amazon Bedrock / Nova Lite - VERIFIED

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

See:

- `docs/bedrock-foundation-model-acceptance-2026-09-01.md`
- `handoff/BEDROCK_FOUNDATION_MODEL_ADDENDUM.md`

## Deep professional workflow

### Phase 1 - autonomous safe work

Five routine actions execute before human attention. Protected activation remains blocked. `vendor-risk` is ready; later authorities are not ready.

### Phase 2 - vendor-risk authority

An external human principal grants `vendor-risk`. The Strands agent resumes activation, ERP sync and purchasing. Payment work remains blocked until `payment-release` becomes ready.

### Phase 3 - payment-release authority

The external principal grants `payment-release`. Payment-profile, terms and remittance-preview work executes. The remittance receipt makes `first-funds` ready. Irreversible transmit remains blocked because `first-funds` is a distinct authority.

### Phase 4 - correction propagation

The principal revokes the earlier `vendor-risk` authority.

Observed canonical state:

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

- region: `eu-central-1`;
- Runtime: `AuthorityCutRuntime`, version `1`;
- status: `READY`;
- direct-code / S3 CodeZip;
- runtime: `PYTHON_3_13`;
- entry point: `agentcore_main.py`;
- network mode: `PUBLIC`;
- packaged source HEAD: `200d71f963bb4496a6f01a6cf1788695b3164739`;
- CodeZip SHA-256: `67c9ce7de97f48970d3c595e6914fef314011fa5cebccf4f01cd4b6bea32690e`.

Real `InvokeAgentRuntime` returned HTTP 200 and passed the Strands loop and authority/correction assertions.

Important historical boundary: that AgentCore Runtime used the deterministic custom Strands provider. Its recorded `FOUNDATION_MODEL_INVOCATION=UNVERIFIED` remains correct for that historical invocation. The 2026-09-01 native Bedrock acceptance is a distinct execution path.

## Devpost live readback - PASS

Authenticated Devpost readback after the Bedrock description update verified:

- project id: `1394239`;
- slug: `authority-cut`;
- project state: `published`;
- project URL: `https://devpost.com/software/authority-cut`;
- video still `https://youtu.be/dY8W-AP4mms`;
- hackathon: `Agents for Humans Hackathon` / `agentsforhumans`;
- submission timestamp remains `2026-08-23T05:14:52.895-04:00`;
- authenticated hackathon relationships remain `registered`, `submitted`;
- live description contains the verified native Bedrock / Nova Lite acceptance and preserves the deterministic-public-proof and historical-AgentCore truth boundaries.

No re-submission, video replacement or public judge URL change was required.

## Current judging-criterion mapping

### Technical Implementation

Lead evidence:

- authentic Strands Agent/tool orchestration;
- exact restricted tool boundary;
- real public execution;
- real native Bedrock / Nova Lite foundation-model execution;
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

## Prior-art boundary

Current Strands already provides HITL interventions, approval interception and interrupt/resume. Agent governance, delegated authority and transactional/compensation patterns also predate this project.

Safe novelty language:

> Authority Cut changes the granularity and lifecycle of human control: compute the smallest currently actionable policy-defined semantic authority surface, keep authority mutation outside the model toolset, and propagate later revocation through already-executed reversible descendants.

No `first`, `unique`, `only`, patentability, alignment-solved or universal-safety claim.

## Pre-existing-work disclosure

Pre-existing EvidenceBound concepts include provenance/evidence binding, dependency graphs, fail-closed verification, selective invalidation/recovery and proof receipts.

This AWS competition repository was created during the submission period. Its vendor-onboarding graph, Authority Cut mechanism, Strands orchestration, evaluation, AgentCore adapter and public judge service are competition-period work. No source file from EvidenceBound Core, Recovery Mesh, Verified Memory, DataHub Gate or SignalReview was copied into this project.

## Historical provider/identity boundaries

- historical optional Vercel AI Gateway provider contract: **PASS**;
- historical Vercel AI Gateway model invocation: **UNRUN**;
- historical reuse of a pre-existing EvidenceBound GitHub OIDC role: `BLOCKED_AWS_OIDC_TRUST`;
- native Amazon Bedrock / Nova Lite foundation-model acceptance: **PASS**.

Do not rewrite historical failed/unrun paths as PASS.

## Final classification

**READY / SUBMITTED / LIVE READBACK PASS.**

Verified limitations:

- real customer productivity/adoption: **UNVERIFIED**;
- arbitrary external-system compensation safety: **UNVERIFIED**;
- general corrigibility/alignment claim: **NOT CLAIMED**.
