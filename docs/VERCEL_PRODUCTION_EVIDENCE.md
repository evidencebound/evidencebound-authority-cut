# Authority Cut — Public Production Evidence

Snapshot: 2026-08-19

## Canonical deployment

- public URL: `https://evidencebound-authority-cut.vercel.app`
- Vercel project: `evidencebound-authority-cut`
- project ID: `prj_WPX42JQ08alE6WfuqlS0xA8XpBzT`
- accepted production deployment: `dpl_7xSMUvRsp8KHjo2J5UqVzMRZBTB9`
- source package commit: `79768810ceda2cf11aeac4a07378d7587cce315c`
- framework/runtime: FastAPI / Python 3.12
- region: `iad1`
- build: **PASS**
- deployment state: **READY**

The deployment installs `authority-cut-agent` directly from the exact public Git commit above and pins `strands-agents==1.52.0`.

## Public acceptance

- `/`: **HTTP 200 PASS**
- `/health`: **HTTP 200 PASS**
- `/api/tool-boundary`: **HTTP 200 PASS**
- `/api/evaluation`: **HTTP 200 PASS**
- `/api/strands-proof-get`: **HTTP 200 PASS**
- `/favicon.ico`: **HTTP 204 PASS**
- `/favicon.png`: **HTTP 204 PASS**

The canonical live proof returned:

```text
execution = REAL_STRANDS_AGENT_LOOP_DETERMINISTIC_MODEL
model_provider = deterministic-public-proof
authority_mutation_tools = []
authority_boundary = EXTERNAL_HUMAN_ONLY
safe_actions_preserved = 5
protected_reversible_effects_rolled_back = 6
irreversible_transmit_after_correction = INVALIDATED
foundation_model_invocation = UNVERIFIED
agentcore = UNVERIFIED
receipt_count = 14
```

## Observed live Strands sequence

Vercel runtime logs for the accepted deployment recorded the real SDK tool loop:

```text
Tool #1: execute_safe_vendor_work
Tool #2: get_authority_cut
External human authority is required before further protected work.
Tool #1: execute_authorized_vendor_work
Tool #2: get_authority_cut
External human authority is required before further protected work.
Tool #1: execute_authorized_vendor_work
Tool #2: get_authority_cut
External human authority is required before further protected work.
```

The public result then showed four phases:

1. safe work complete; only `vendor-risk` ready;
2. external principal grants `vendor-risk`; protected reversible vendor work executes; `payment-release` becomes ready;
3. external principal grants `payment-release`; remittance preview executes; `first-funds` becomes the sole ready authority while `transmit` remains `BLOCKED`;
4. external principal revokes `vendor-risk`; six reversible protected effects become `ROLLED_BACK`, five unrelated safe actions remain `EXECUTED`, and irreversible `transmit` becomes `INVALIDATED`.

## Authority boundary

Public `/api/tool-boundary` returned exactly:

- model-callable tools:
  - `execute_safe_vendor_work`
  - `get_authority_cut`
  - `execute_authorized_vendor_work`
- authority mutation tools: **none**
- principal actions: `approve`, `revoke`
- principal channel: `EXTERNAL_HUMAN_API`

This is the core human-control boundary. The model can request work and inspect the authority cut; it cannot grant or revoke its own authority.

## Evaluation surface

Public `/api/evaluation` returned the fixed-workflow controlled metrics:

- protected effects: 7
- per-effect HITL baseline prompts: 7
- policy-defined Authority Cut decisions: 3
- prompt reduction: `0.5714285714` (57.14%)
- safe actions before human intervention: 5
- reversible effects executed before correction: 6
- reversible effects rolled back after correction: 6
- irreversible effects executed without funds-release authority: 0
- unaffected safe actions preserved: 5

These are fixed-workflow controlled metrics, not generalized user-productivity claims.

## Public CI evidence

PR #4 CI run `32219499297` passed:

- deterministic kernel on Python 3.11: **PASS**
- deterministic kernel on Python 3.12: **PASS**
- deterministic kernel on Python 3.13: **PASS**
- actual `strands-agents==1.52.0` install: **PASS**
- published Agent construction: **PASS**
- real Strands Agent loop with deterministic custom Model: **PASS**
- deployable public Strands judge surface: **PASS**
- exact Vercel entrypoint acceptance alias: **PASS**
- source snapshot: **PASS**

## Truth boundary

The live production service proves:

- real Strands SDK Agent/tool orchestration;
- real tool execution against the competition workflow;
- selective human intervention;
- explicit external human authority boundary;
- correction propagation;
- compensation of reversible effects;
- fail-closed gating of the irreversible transfer;
- public judge accessibility.

It does **not** yet prove:

- a foundation-model-backed Strands run;
- Amazon Bedrock AgentCore deployment.

Those remain separately classified and must not be inferred from the production Strands proof.
