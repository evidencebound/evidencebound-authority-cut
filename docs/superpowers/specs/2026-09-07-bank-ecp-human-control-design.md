# Authority Cut Banking Human Control Design

## Outcome

Turn Authority Cut from a technically strong control-plane demo into a banking product a judge can understand immediately:

> A bank lets an AI onboard a vendor. The AI does the routine work. A human approves the risky decision. If the evidence changes, affected work is undone and payment stays blocked.

## User and problem

Primary user: bank third-party risk, vendor-risk, compliance, procurement, or operational-risk professional.

The failure mode is not that an AI cannot ask for approval. It is that autonomous work can continue after the evidence supporting a previously approved consequential decision becomes stale, contradicted, unsupported, or otherwise invalid.

Authority Cut must make the correction operational rather than conversational.

## Product behavior

The judge path is a vendor-onboarding workflow with three layers:

1. **Routine work** — the Strands agent completes safe onboarding work without human interruption.
2. **Evidence-gated risky decision** — a narrow BANK-ECP-derived DORA evidence check determines whether the vendor-risk decision is supportable enough to ask the human to approve it. Model confidence never creates authority.
3. **Correction propagation** — when the evidence package changes from supported to HOLD/ABSTAIN, previously granted vendor-risk authority becomes stale. Affected reversible descendants are compensated, unrelated safe work remains, and the first irreversible payment remains blocked.

## BANK-ECP bridge

Do not embed the private BANK-ECP benchmark runtime or expose protected benchmark internals.

Publish one sanitized development-only bridge fixture derived from BANK-ECP's DORA third-party-risk family:

- authoritative source: Regulation (EU) 2022/2554 (DORA), Article 28(1)(a);
- supported conclusion: a financial entity remains responsible for its DORA/applicable-financial-services-law obligations when using ICT third-party services;
- changed/defective evidence package: an unsupported reversal claiming the ICT vendor assumes the financial entity's statutory responsibility;
- supported result: `PASS`;
- defective result: `HOLD` with a material-support reason;
- evidence classification: `DEVELOPMENT_ONLY`, `NOT_FORMAL_BENCHMARK_EVIDENCE`, no model-performance claim.

The bridge is load-bearing: the `vendor-risk` human authority cannot be granted unless its BANK-ECP evidence gate is `PASS`; a later non-PASS result invalidates stale authority and triggers the existing selective rollback path.

## Runtime design

Add core evidence-gate state to the Authority Cut runtime:

- evidence verdicts: `PASS`, `HOLD`, `ABSTAIN`;
- an evidence decision records gate id, case id, verdict, reasons, source locator, evidence class, and digest;
- `DecisionBundle` may declare an optional `evidence_gate`;
- the `vendor-risk` bundle declares the BANK-ECP bridge gate;
- `decision_surface()` reports both prerequisite readiness and evidence readiness;
- `decide(... approved=True ...)` fails closed unless required evidence is `PASS`;
- applying a new non-PASS evidence decision to an already-approved bundle invalidates that authority and reuses selective rollback/compensation;
- human grant/revoke remains outside the model-callable Strands tool surface.

No new approve/revoke/correct authority tool is exposed to the model.

## Public API and product surface

Add a narrow banking path to the public service:

- start/reset vendor onboarding;
- run routine work;
- evaluate the supported BANK-ECP bridge evidence;
- human approves vendor risk;
- human approves payment profile where needed to make downstream effects visible;
- correct the evidence package to a HOLD case;
- surface rollback, preserved safe work, and blocked/invalidated first payment.

The first screen must not lead with control-kernel status, semantic bundles, fixed metrics, receipts, or architecture.

Opening copy:

> **Onboard a vendor without giving the AI the final say.**
>
> The AI handles routine vendor work. You approve decisions that carry real compliance or financial risk. If the evidence changes later, affected work is undone and payment stays blocked.

Primary visible sequence:

1. `AI working`
2. `Human decision`
3. `Evidence changed`
4. `Affected work undone`
5. `Safe work preserved`
6. `First payment blocked`

Technical truth and diagnostics remain available below the product story.

## README and Devpost narrative

Public order:

1. human problem;
2. user outcome;
3. working product;
4. visible magic moment;
5. business relevance;
6. Strands/AWS;
7. BANK-ECP/EvidenceBound invention;
8. technical evidence;
9. limitations.

Do not remove historical Bedrock/AgentCore acceptance evidence or alter PASS/UNVERIFIED boundaries.

## Testing and acceptance

### Runtime

- vendor-risk approval is rejected before BANK-ECP evidence PASS;
- supported DORA bridge case produces PASS and makes vendor-risk evidence-ready;
- defective/corrected bridge case produces HOLD;
- PASS -> HOLD after human approval invalidates stale vendor-risk authority;
- affected reversible protected actions roll back;
- safe actions remain EXECUTED;
- irreversible first payment never executes under stale authority;
- model-callable Strands tool set remains unchanged.

### Product

- first-screen HTML contains the banking user/problem/outcome language before diagnostics;
- public API exposes current BANK-ECP evidence status and correction outcome;
- legacy technical endpoints remain truthful.

### External acceptance

- CI green on the exact release commit;
- Vercel production points to that commit and `/health` is healthy;
- browser smoke proves the 5-second and 60-second story;
- Devpost/README/video use the same banking narrative;
- any new thumbnail, YouTube image, or hackathon visual asset is created strictly through Google Slides, not image generation or Canva.

## Evidence boundary

BANK-ECP bridge fixtures are development-only product integration evidence. They are not formal holdout results and do not demonstrate model superiority, legal advice, regulatory certification, customer adoption, ROI, or general productivity gains.

EUR-Lex Article 28(1)(a) is the authoritative legal source for the public DORA statement.
