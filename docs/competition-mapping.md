# AWS Agents for Humans — Judge Mapping

Snapshot: 2026-08-19

Current Stage Two criteria are equally weighted: **Technical Implementation, Design, Potential Impact, Creativity & Originality, Presentation**. Technical Implementation is the first tie-break criterion.

## Technical Implementation

Strongest verified evidence:

- Strands is architecturally central, not cosmetic;
- `strands-agents==1.52.0` installs in public CI;
- published `Agent` construction: **PASS**;
- real Strands Agent/tool loop: **PASS** in GitHub Actions and public Vercel production;
- model-callable tools are exactly three non-authorizing operations;
- approve/revoke authority mutations are absent from the model tool set;
- one deep vendor-onboarding workflow executes end-to-end;
- five safe actions execute autonomously before human attention;
- policy-defined Authority Cut exposes only ready semantic human decisions;
- external human grants change what downstream protected work can execute;
- correction/revocation propagates through already-executed descendants;
- six reversible protected effects compensate/roll back after the correction;
- five unrelated safe actions remain executed;
- irreversible transmit remains separately gated and becomes `INVALIDATED` after upstream correction;
- deterministic evidence receipts and authority state are inspectable;
- Python 3.11 / 3.12 / 3.13 public CI: **PASS**;
- exact public deployment from the current public source revision: **PASS**;
- public live judge path: **PASS**.

Non-blocking score upgrades:

- foundation-model-backed Strands acceptance: **UNRUN / BLOCKED_RUNTIME_GATEWAY_CREDENTIAL**;
- AgentCore deployment: **UNRUN / BLOCKED_AWS_OIDC_TRUST**.

AgentCore remains optional and should be added only if an authenticated deployment can be accepted without weakening the human-control boundary.

## Design

The design target is **Decision Surface Compression + Reversible Autonomy**, not a generic approval chatbot.

The agent autonomously completes safe routine work, then surfaces only the smallest policy-valid semantic authority set needed for currently reachable protected effects. Human authority is explicitly external to the model. Later correction changes downstream execution state rather than merely adding an audit note.

The live judge surface makes the boundaries visible:

1. safe work executes;
2. `vendor-risk` becomes ready;
3. later authorities remain future/not-ready;
4. human grant permits protected reversible work;
5. `payment-release` becomes ready only after its prerequisite;
6. first-funds remains separate and irreversible;
7. revocation rolls back reversible descendants and invalidates transmit while unrelated safe work is preserved.

## Potential Impact

Target users are professional operations teams where autonomous agents can reduce routine workload but should not silently acquire spending, compliance or exception authority.

Potential domains include procurement, vendor onboarding, finance operations, insurance operations and other multi-step enterprise workflows with reversible and irreversible effects.

Verified fixed-workflow metric:

- per-protected-effect HITL baseline: 7 prompts;
- Authority Cut decisions: 3;
- controlled prompt reduction: **57.14%**;
- safe actions completed before interruption: 5.

This is not a generalized productivity result. Real user time savings, adoption and policy correctness remain unmeasured.

## Creativity & Originality

The competition thesis is the combination of:

- policy-defined **Authority Cut Sets** that compress human attention to semantic authority decisions rather than one prompt per tool effect; and
- **Reversible Correction Propagation** that changes already-executed downstream state when a principal later revokes an upstream authority.

This is deliberately narrower than claiming invention of HITL, approval workflows, provenance, compensation transactions or dependency graphs. Prior-art overlap and pre-existing EvidenceBound concepts are disclosed.

## Presentation

Current presentation assets:

- public repository;
- architecture documentation and Mermaid source;
- public CI;
- public production URL: `https://evidencebound-authority-cut.vercel.app`;
- live one-click Strands execution path;
- machine-readable tool-boundary and evaluation endpoints;
- claims ledger;
- production evidence ledger;
- exact AWS/Gateway blockers;
- pre-existing-work disclosure;
- Judge Pack and final Devpost checklist.

Final media should show the four-phase live path rather than spending video time on infrastructure. The memorable proof is: **the model can execute work and inspect authority, but it cannot approve itself; a later human correction changes downstream execution and preserves unrelated work.**

## Tie-break strategy

Because Technical Implementation is the first tie-break, the strongest order of evidence is:

1. live public real Strands Agent/tool execution;
2. explicit absence of authority mutation tools;
3. actual downstream state change after human grants and revocation;
4. irreversible-effect gate;
5. reproducible public CI/source provenance;
6. optional AgentCore/foundation-model upgrades only if they can be verified without destabilizing items 1–5.
