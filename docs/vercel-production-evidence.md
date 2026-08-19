# Authority Cut — Vercel Production Evidence

Snapshot: 2026-08-19

## Canonical public judge service

- URL: `https://evidencebound-authority-cut.vercel.app`
- Vercel project: `evidencebound-authority-cut`
- project ID: `prj_WPX42JQ08alE6WfuqlS0xA8XpBzT`
- canonical source commit installed by the deployment: `1cf640d735d822f3a66c517e5eeb8711fec2a040`
- accepted deployment: `dpl_8b5jXwdhD57u2b4XfvWNRJSLsrey`
- framework/runtime: FastAPI / Python 3.12
- region: `iad1`
- build: **PASS**
- deployment state: **READY**

The deployment installs `authority-cut-agent` directly from the exact public Git commit above and pins `strands-agents==1.52.0`. The optional Gateway adapter may exist in the package, but **no Gateway/model route is attached to the public judge service**.

## Public acceptance

- `/health`: **HTTP 200 PASS**
- `/api/tool-boundary`: **HTTP 200 PASS**
- `/api/evaluation`: **HTTP 200 PASS**
- `/api/strands-proof-get`: **HTTP 200 PASS**
- judge root/UI: **HTTP 200 PASS**

Canonical `/api/strands-proof-get` result:

```text
execution = REAL_STRANDS_AGENT_LOOP_DETERMINISTIC_MODEL
model_provider = deterministic-public-proof
strands_tools = [execute_safe_vendor_work, get_authority_cut, execute_authorized_vendor_work]
authority_mutation_tools = []
authority_boundary = EXTERNAL_HUMAN_ONLY
safe_actions_preserved = 5
protected_reversible_effects_rolled_back = 6
irreversible_transmit_after_correction = INVALIDATED
foundation_model_invocation = UNVERIFIED
agentcore = UNVERIFIED
receipt_count = 14
```

## Live four-phase state proof

### Phase 1 — safe work and authority cut

Five safe actions were `EXECUTED` while `activate` remained `BLOCKED`. `vendor-risk` was ready; `payment-release` and `first-funds` were not ready.

### Phase 2 — external vendor-risk grant

The principal grant was applied outside the Strands tool set. The agent resumed authorized reversible vendor work. `activate`, ERP sync and purchasing executed; payment effects remained gated. `payment-release` became ready.

### Phase 3 — external payment-release grant

The principal grant was again external. Payments/terms/remittance executed, producing the prerequisite evidence for `first-funds`. `first-funds` became the sole ready authority and irreversible `transmit` remained `BLOCKED`.

### Phase 4 — external correction

The principal revoked `vendor-risk`. The affected set included six reversible protected descendants plus transmit. The six reversible effects became `ROLLED_BACK`; transmit became `INVALIDATED`; all five unrelated safe actions remained `EXECUTED`.

## Runtime trace

Vercel runtime logs for the accepted deployment observed the real Strands SDK sequence:

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

This runtime trace is important evidence that the public service is executing the Strands Agent/tool loop rather than returning only a precomputed JSON fixture.

## Human-control boundary

Public `/api/tool-boundary` reports:

- model-callable tools: exactly three execution/inspection tools;
- authority mutation tools: none;
- principal actions: approve/revoke;
- principal channel: external human API.

The public proof uses reset-each-call synthetic in-memory workflow state and creates no real vendor or payment effect.

## Truth boundary

This production evidence proves authentic Strands SDK orchestration/tool execution and the Authority Cut control semantics. It does **not** prove foundation-model quality or AgentCore behavior. Those are tracked separately in `foundation-model-boundary.md` and `aws-capability-boundary.md`.
