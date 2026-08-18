# Authority Cut — Reversible Autonomy with Strands Agents

**One-line pitch:** A professional agent completes routine work autonomously, then exposes the smallest **policy-valid semantic authority set** needed for protected downstream effects; a later human correction propagates through already-executed reversible descendants without erasing unrelated work.

## Controlled evidence available now

The competition-period control kernel implements one deep vendor-onboarding workflow:

- 5 safe actions execute before human attention is required;
- 7 protected tool effects are governed by 3 policy-defined human authority decisions;
- the controlled per-protected-effect baseline is therefore 7 prompts versus 3 Authority Cut decisions (`57.14%` fewer prompts in this fixed workflow);
- first-funds remains a distinct irreversible authority and cannot be approved before its remittance-preview prerequisite exists;
- after vendor-risk authority is revoked, 6 executed reversible protected effects are compensated while the pending irreversible transfer is invalidated;
- the Strands model-callable tool set contains **no approve or revoke function**.

These are controlled mechanism results, not general productivity or safety claims.

```bash
python -m pip install -e '.[dev]' --no-build-isolation
PYTHONPATH=src pytest
PYTHONPATH=src python scripts/run_demo.py
PYTHONPATH=src python scripts/run_evaluation.py
PYTHONPATH=src uvicorn authority_cut.api:app --host 127.0.0.1 --port 8080
```

## Strands boundary

`authority_cut.strands_app` is the competition-period Strands orchestration adapter. Its model-callable tools are exactly:

1. `execute_safe_vendor_work`
2. `get_authority_cut`
3. `execute_authorized_vendor_work`

Human approve/revoke operations are external principal actions exposed by the API, not agent tools. The API and Strands adapter share the same process-local `ControlPlane`, so externally recorded authority changes are the state the agent observes when it resumes.

Public GitHub Actions now verifies more than import compatibility: it installs the real `strands-agents` SDK, constructs the published `Agent`, and executes the real Strands Agent loop through all three published tools using a deterministic custom Strands `Model` provider. The trace proves safe work, authority-surface inspection, externally granted resume, and correction/rollback while the model tool set has no authority mutation function.

That CI proof establishes **real Strands SDK orchestration/tool execution**, but not foundation-model quality. A Bedrock/other foundation model has not yet executed the full workflow, so foundation-model invocation remains `BLOCKED/UNVERIFIED`.

## Public verification

- deterministic tests: **21/21 PASS** locally and on public GitHub Actions;
- Python 3.11 / 3.12 / 3.13 CI lanes: **PASS**;
- `strands-agents` install: **PASS** in public CI;
- Strands `Agent` construction: **PASS** in public CI;
- real Strands Agent loop with deterministic custom Model provider: **PASS**;
- all three published model-callable tools executed through Strands: **PASS**;
- model toolset authority mutation check: **PASS**;
- foundation-model invocation: **BLOCKED / UNVERIFIED**;
- AgentCore deployment: **BLOCKED / UNVERIFIED**;
- public judge endpoint: **BLOCKED / UNVERIFIED**.

See `qa/QA_RECEIPT.json` and `handoff/AWS_JUDGE_PACK.md`.

## AgentCore

AgentCore is an advantageous deployment target, not a claimed integration. See `docs/agentcore-decision.md`.

## New-project boundary

This source tree was authored for the AWS competition period. The dedicated public repository was created on 2026-08-18, after the competition submission period opened. Pre-existing EvidenceBound concepts are disclosed in `docs/preexisting-work.md`; no source file from EvidenceBound Core, Recovery Mesh, Verified Memory, DataHub Gate, or SignalReview is copied here. The initial GitHub commit is preserved as the parent of the published competition source so repository timing remains auditable.

## Trust boundary

Authority Cut does not prove policy correctness, legal authorization, safe compensation in arbitrary external systems, or general corrigibility. Minimality is exact only over the policy-defined semantic decision bundles supplied to the runtime.
