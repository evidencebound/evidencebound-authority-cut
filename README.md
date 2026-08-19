# Authority Cut — Reversible Autonomy with Strands Agents

**One-line pitch:** A professional agent completes routine work autonomously, exposes only the smallest policy-valid semantic human authorities for protected effects, and propagates later human correction through already-executed reversible descendants without erasing unrelated safe work.

## Submission readiness — READY

Authority Cut is engineering-ready for **AWS Agents for Humans** except for final registration/media/form work. The required Strands integration, real tool execution, deep professional workflow, selective human intervention, correction propagation, reversible recovery, irreversible-action gating, provenance, public repository, public CI, and live public judge path are implemented and verified.

Public judge URL:

`https://evidencebound-authority-cut.vercel.app`

Public repository:

`https://github.com/moneyparking/evidencebound-authority-cut`

Two score-upgrade paths remain deliberately separate from project completion:

- foundation-model-backed Strands acceptance: **UNRUN / BLOCKED_RUNTIME_GATEWAY_CREDENTIAL**;
- Amazon Bedrock AgentCore deployment: **BLOCKED_AWS_OIDC_TRUST**.

Neither is represented as completed. AgentCore is optional under the current competition rules; the public submission path already executes the real Strands SDK Agent/tool loop. The repository contains a fail-closed optional foundation-model adapter so that acceptance can be rerun if a runtime credential becomes available without changing the Authority Cut semantics.

## What the live path proves

The fixed vendor-onboarding workflow contains:

- **5 safe actions** that execute before human attention;
- **7 protected effects** governed by **3 policy-defined semantic authority decisions**;
- a controlled baseline of 7 per-effect prompts versus 3 Authority Cut decisions (`57.14%` fewer prompts in this fixed workflow);
- a distinct `first-funds` irreversible authority that cannot become ready until a remittance-preview receipt exists;
- correction propagation that compensates **6 already-executed reversible protected effects** after `vendor-risk` is revoked;
- preservation of all **5 unrelated safe actions** after the correction;
- invalidation of the pending irreversible transfer rather than pretending it was rolled back;
- a Strands model-callable tool set containing **no approve or revoke function**.

These are controlled fixed-workflow results, not generalized safety or productivity claims.

## Real Strands execution

The model-callable Strands tools are exactly:

1. `execute_safe_vendor_work`
2. `get_authority_cut`
3. `execute_authorized_vendor_work`

Human approve/revoke operations are external principal actions. They are not present in the Strands tool schema.

Public GitHub Actions installs `strands-agents==1.52.0`, constructs the published `Agent`, and executes the real Strands Agent loop through the three tools using a deterministic custom Strands `Model` provider. The deployable public surface is tested through that same loop.

The live Vercel judge path then executes the real Strands loop again. Its accepted proof returned:

```text
execution = REAL_STRANDS_AGENT_LOOP_DETERMINISTIC_MODEL
authority_mutation_tools = []
authority_boundary = EXTERNAL_HUMAN_ONLY
safe_actions_preserved = 5
protected_reversible_effects_rolled_back = 6
irreversible_transmit_after_correction = INVALIDATED
receipt_count = 14
```

Vercel runtime logs also observed the real tool-call sequence: safe execution -> authority-cut inspection -> externally authorized resume -> next authority cut -> externally authorized resume -> correction propagation.

## Public judge path

Open:

`https://evidencebound-authority-cut.vercel.app`

Then run **Run live Strands judge path**. The page executes a reset-each-call synthetic vendor workflow and displays the execution ledger.

Machine-readable routes:

- `/health`
- `/api/tool-boundary`
- `/api/evaluation`
- `POST /api/strands-proof`
- `/api/strands-proof-get` — acceptance alias for automated verification

The live proof uses only synthetic in-memory workflow state and does not create external vendor/payment effects.

## Controlled evidence

```bash
python -m pip install -e '.[dev]' --no-build-isolation
PYTHONPATH=src pytest
PYTHONPATH=src python scripts/run_demo.py
PYTHONPATH=src python scripts/run_evaluation.py
PYTHONPATH=src uvicorn authority_cut.api:app --host 127.0.0.1 --port 8080
```

Public CI gates:

- deterministic kernel Python 3.11: **PASS**;
- deterministic kernel Python 3.12: **PASS**;
- deterministic kernel Python 3.13: **PASS**;
- compile gate: **PASS**;
- actual Strands SDK install: **PASS**;
- Strands Agent construction: **PASS**;
- real Strands deterministic-model Agent loop: **PASS**;
- deployable public Strands judge surface: **PASS**;
- exact Vercel entrypoint acceptance: **PASS**;
- optional OpenAI-compatible Strands provider install: **PASS**;
- optional Gateway path without runtime credential fails closed before network/model execution: **PASS**.

## Foundation-model boundary

The optional adapter in `authority_cut.gateway_proof` is wired for a Strands `OpenAIModel` against an OpenAI-compatible gateway while retaining the exact same three non-authorizing tools and external-human authority mutations.

Its no-network CI contract passes. A protected Vercel acceptance attempt showed that the directly deployed runtime had neither `AI_GATEWAY_API_KEY` nor `VERCEL_OIDC_TOKEN`; the proof therefore failed closed before any gateway/model request. The transient model-call route was subsequently removed and replaced by a receipt-only surface.

Correct status:

- provider integration contract: **PASS**;
- actual foundation-model invocation: **UNRUN**;
- blocker: **RUNTIME_GATEWAY_CREDENTIAL_UNAVAILABLE**;
- model spend reached: **NO**.

Do not infer foundation-model quality from the deterministic live proof.

## AgentCore boundary

AgentCore remains a valuable Technical Implementation upgrade, but not a claimed integration. A non-mutating GitHub OIDC probe against the existing EvidenceBound AWS deployment role returned `Not authorized to perform sts:AssumeRoleWithWebIdentity` for the new Authority Cut repository identity. No Bedrock discovery, model invocation, or AWS resource mutation was attempted after that denial.

Correct status:

- AgentCore architecture/evaluation: **prepared**;
- authenticated AWS deployment: **BLOCKED_AWS_OIDC_TRUST**;
- AWS resource mutation by the probe: **UNRUN**;
- paid AWS model invocation by the probe: **UNRUN**.

See `docs/agentcore-decision.md` and `docs/aws-capability-boundary.md`.

## New-project / pre-existing-work boundary

This source tree was authored for the AWS competition period. The dedicated public repository was created after the competition submission period opened. Pre-existing EvidenceBound concepts — provenance/evidence binding, dependency graphs, fail-closed verification, selective invalidation/recovery and proof receipts — are disclosed in `docs/preexisting-work.md`.

No source file from EvidenceBound Core, Recovery Mesh, Verified Memory, DataHub Gate or SignalReview is copied into this project. The original GitHub initial commit is preserved as the parent of the competition source publication so repository timing remains auditable.

## Trust boundary

Authority Cut does not prove policy correctness, legal authorization, safe compensation in arbitrary external systems, authenticated principal identity, distributed durable authority state, general corrigibility, or generalized productivity improvement. Minimality is exact only over the policy-defined semantic decision bundles supplied to the runtime.

See `handoff/AWS_JUDGE_PACK.md`, `handoff/DEVPOST_FINAL_CHECKLIST.md`, `docs/claims-ledger.md`, and `qa/QA_RECEIPT.json`.
