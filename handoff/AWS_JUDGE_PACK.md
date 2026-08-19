# AWS Agents for Humans — Final Submission Handoff

Snapshot: 2026-08-19

## Decision

**READY** — Authority Cut is engineering/judge-path ready except for final registration, video/media and Devpost form submission. The optional foundation-model and AgentCore upgrades remain explicitly unverified and are not required to demonstrate the core competition contribution.

## Identity

**Canonical project name:** Authority Cut

**Track:** Professional Agents

**One-line pitch:** A Strands professional agent completes routine work autonomously, surfaces only the smallest policy-valid semantic human authorities for protected downstream effects, and propagates a later human correction through reversible execution without erasing unrelated safe work.

**Invention thesis:** **Authority Cut Sets + Reversible Correction Propagation.**

Public repository:

`https://github.com/moneyparking/evidencebound-authority-cut`

Public judge URL:

`https://evidencebound-authority-cut.vercel.app`

## What judges can verify live

Open the public URL and select **Run live Strands judge path**.

The production service executes the real Strands SDK Agent/tool loop against a reset-each-call synthetic vendor-onboarding workflow. It does not replay a saved result.

Canonical production evidence:

- Vercel project: `evidencebound-authority-cut`;
- project ID: `prj_WPX42JQ08alE6WfuqlS0xA8XpBzT`;
- source commit installed by production: `1cf640d735d822f3a66c517e5eeb8711fec2a040`;
- accepted deployment: `dpl_8b5jXwdhD57u2b4XfvWNRJSLsrey`;
- `/health`: **PASS / HTTP 200**;
- `/api/tool-boundary`: **PASS / HTTP 200**;
- `/api/evaluation`: **PASS / HTTP 200**;
- `/api/strands-proof-get`: **PASS / HTTP 200**;
- runtime Strands tool trace: **PASS**.

Canonical live result:

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

## Deep workflow

### Phase 1 — autonomous safe work

The agent executes five routine safe actions before human attention:

1. collect vendor packet;
2. tax check;
3. bank check;
4. draft vendor record;
5. follow-up preparation.

Protected activation remains blocked.

The current Authority Cut exposes `vendor-risk` as ready. `payment-release` and `first-funds` remain future/not-ready.

### Phase 2 — vendor-risk authority

An **external human principal**, not the model, grants the semantic `vendor-risk` decision.

The Strands agent resumes only work authorized by that recorded grant. Activation, ERP sync and purchasing execute. Payment-related effects remain blocked. `payment-release` becomes ready.

### Phase 3 — payment-release authority

The external principal grants `payment-release`.

The agent resumes payment profile, terms and remittance-preview work. The remittance receipt makes `first-funds` ready. The irreversible `transmit` effect remains `BLOCKED` because `first-funds` is a separate authority.

### Phase 4 — correction propagation

The principal revokes the earlier `vendor-risk` authority.

Authority Cut propagates the correction through already-executed descendants:

- 6 reversible protected effects -> `ROLLED_BACK`;
- pending irreversible transmit -> `INVALIDATED`;
- 5 unrelated safe actions -> remain `EXECUTED`.

This is the core human-control demonstration: correction changes downstream execution state rather than merely appending an audit note.

## Authority boundary

The model-callable Strands tool set is exactly:

1. `execute_safe_vendor_work`
2. `get_authority_cut`
3. `execute_authorized_vendor_work`

There is **no approve/revoke tool**.

Human grant/revocation is an external principal action. The model can execute permitted work and inspect the decision surface; it cannot mint its own authority through the published tool interface.

## Fixed-workflow evaluation

Verified controlled metrics:

- safe actions before human intervention: **5**;
- protected effects: **7**;
- per-protected-effect HITL baseline prompts: **7**;
- policy-defined semantic Authority Cut decisions: **3**;
- fixed-workflow prompt reduction: **57.14%**;
- reversible protected effects executed before correction: **6**;
- reversible protected effects rolled back after correction: **6**;
- irreversible effects executed without `funds_release`: **0**;
- unaffected safe actions preserved: **5**.

Do not generalize the 57.14% figure beyond this fixed workflow. No field-study productivity claim is made.

## Public CI evidence

Current accepted gates include:

- Python 3.11 deterministic kernel: **PASS**;
- Python 3.12 deterministic kernel: **PASS**;
- Python 3.13 deterministic kernel: **PASS**;
- 21/21 deterministic tests: **PASS**;
- compile gate: **PASS**;
- `strands-agents==1.52.0` install: **PASS**;
- Strands Agent construction: **PASS**;
- real Strands Agent loop with deterministic custom Model provider: **PASS**;
- all three published tools executed through the SDK loop: **PASS**;
- deployable public Strands surface: **PASS**;
- Vercel entrypoint acceptance alias: **PASS**;
- OpenAI-compatible Strands provider install/contract: **PASS**;
- missing runtime foundation-model credential fails closed before provider execution: **PASS**.

Canonical optional-provider CI run: `32220265475`.

## Current judging-criterion mapping

### 1. Technical Implementation

Lead evidence:

- authentic Strands Agent/tool orchestration in public production;
- real tool execution, not a chat-only interface;
- one deep professional workflow;
- explicit human/model capability boundary;
- prerequisite/receipt-gated authority decisions;
- downstream correction propagation and reversible compensation;
- separately gated irreversible effect;
- public CI, source provenance and runtime trace.

Optional score upgrades are documented below rather than overstated.

### 2. Design

Authority Cut compresses the human decision surface rather than interrupting the operator for each protected tool effect. The UI shows what is autonomous, what authority is ready now, what remains future, and what a correction changed.

### 3. Potential Impact

Target problem: professional agents should automate routine work without silently acquiring exception, payment or irreversible-action authority.

Commercial hypothesis: reusable human-control middleware for procurement, vendor onboarding, finance operations, insurance operations and other multi-step enterprise agent workflows.

Real adoption/productivity remains unverified.

### 4. Creativity & Originality

The competition contribution is the concrete combination of:

- semantic policy-defined Authority Cut computation; and
- post-approval correction propagation over already-executed reversible descendants.

Do not claim invention of HITL, provenance graphs, compensation transactions, dependency invalidation or approval workflows generally.

### 5. Presentation

Strongest presentation path is a live four-phase proof in under five minutes. Show the tool boundary and correction effect visually; do not spend the video on infrastructure setup.

## Pre-existing-work disclosure

Pre-existing EvidenceBound concepts include provenance/evidence binding, dependency graphs, fail-closed verification, selective invalidation/recovery and proof receipts.

This AWS competition repository was created during the submission period. Its vendor-onboarding action graph, Authority Cut mechanism, Strands orchestration, evaluation and public judge service are competition-period implementation. No source file from EvidenceBound Core, Recovery Mesh, Verified Memory, DataHub Gate or SignalReview was copied into this project.

The original GitHub initial commit remains in repository history so project timing is auditable.

See `docs/preexisting-work.md` and `docs/repository-provenance.md`.

## Optional score-upgrade boundary A — foundation model

Status:

- optional Strands `OpenAIModel` adapter: **PASS**;
- pinned provider install/CI contract: **PASS**;
- actual foundation-model invocation: **UNRUN**;
- blocker: **BLOCKED_RUNTIME_GATEWAY_CREDENTIAL**.

A direct Vercel acceptance runtime had neither `AI_GATEWAY_API_KEY` nor `VERCEL_OIDC_TOKEN`. The fail-closed credential guard stopped execution before any Gateway/model request; no model request or model spend reached the Gateway.

The transient acceptance route was removed. The auxiliary project is now receipt-only.

Do not claim foundation-model execution unless a future authenticated acceptance run actually passes all state assertions.

## Optional score-upgrade boundary B — AgentCore

Status:

- AgentCore design/evaluation: prepared;
- authenticated AgentCore deployment: **UNRUN**;
- blocker: **BLOCKED_AWS_OIDC_TRUST**.

Non-mutating capability probe:

- GitHub Actions run `32219855151`;
- candidate role `arn:aws:iam::877348951762:role/EvidenceBoundGitHubDeployRole`;
- `sts:AssumeRoleWithWebIdentity`: **BLOCKED / Not authorized**;
- Bedrock discovery: **UNRUN**;
- paid model invocation: **UNRUN**;
- AWS resource mutation: **UNRUN**.

AgentCore is optional. Do not weaken the authority boundary or destabilize the live judge path merely to add it.

## Competition / compliance essentials

Current competition window closes **2026-09-14 17:00 PT / 2026-09-15 00:00 UTC**.

Submission requirements to preserve:

- Strands must remain architecturally central;
- project must be new during the competition period;
- public source repository;
- README and architecture documentation;
- MIT or Apache license — this repo uses Apache-2.0;
- public demo/testing path;
- public YouTube/Vimeo demo video, maximum five minutes;
- AWS Builder ID;
- disclose pre-existing work.

Registered participants may request the competition AWS promotional credit while the organizer offer remains available; current deadline is **2026-09-11 12:00 PT**. This is useful only if the optional AWS/AgentCore upgrade is pursued.

## Video capture path

Recommended sequence:

1. **Problem, 15–20 sec:** agents either interrupt too often or silently accumulate authority.
2. **Tool boundary:** show exactly three Strands tools and no approve/revoke tool.
3. **Run live path:** five safe actions execute automatically.
4. **Authority Cut:** vendor-risk ready; later decisions not ready.
5. **External grant:** vendor-risk -> agent resumes protected reversible work.
6. **Second grant:** payment-release -> remittance preview; first-funds ready; transmit still blocked.
7. **Correction:** revoke vendor-risk -> six rollbacks + transmit invalidated + five safe actions preserved.
8. **Evidence:** live runtime/receipt states and public source/CI.
9. **Close:** Authority Cut = compressed human authority plus reversible correction propagation; explicit limitations.

## Strongest safe claims

Use:

- “The published Strands tool set contains no authority mutation tool.”
- “The public judge URL executes the real Strands Agent/tool loop.”
- “In this fixed workflow, seven protected effects are governed by three semantic human authorities.”
- “A later human revocation rolls back six executed reversible descendants while preserving five unrelated safe actions.”
- “The irreversible transfer remains separately gated and becomes invalidated after the upstream correction.”

Avoid:

- “the model can never self-approve” as a universal statement beyond the published interface;
- “first/unique/only” without stronger prior-art proof;
- “solves alignment/corrigibility/agent safety”;
- generalized 57.14% productivity claims;
- AgentCore or foundation-model execution claims before real acceptance.

## Remaining owner/media actions

Engineering status is **READY**. Remaining required user-facing actions are:

- confirm/register for the hackathon and accept official terms if not already registered;
- ensure AWS Builder ID is available for submission;
- record/edit/publish the <=5 minute public video;
- enter public repo and judge URL in Devpost;
- include the pre-existing-work disclosure;
- submit the Devpost entry.

Optional only:

- request AWS competition credits and fix repository OIDC trust if AgentCore is pursued;
- provide a supported runtime model credential and rerun protected foundation-model acceptance;
- publish up to three eligible builder.aws technical posts if pursuing the current bonus-score opportunity.

## Final classification

**Authority Cut: READY for submission except final media/forms.**

Optional score-upgrade limitations:

- foundation-model execution: **UNRUN / BLOCKED_RUNTIME_GATEWAY_CREDENTIAL**;
- AgentCore deployment: **UNRUN / BLOCKED_AWS_OIDC_TRUST**.

These limitations must remain visible, but they do not negate the verified live Strands professional-agent submission path.
