# Authority Cut — Foundation-Model Acceptance Boundary

Snapshot: 2026-08-19

## Objective

Test whether the exact Authority Cut tool/control boundary can be driven by a real foundation model without giving the model any approve/revoke capability and without exposing a paid model endpoint on the public judge service.

## Prepared provider path

The optional adapter uses:

- Strands `OpenAIModel`;
- pinned `strands-agents[openai]==1.52.0`;
- OpenAI-compatible gateway base URL `https://ai-gateway.vercel.sh/v1`;
- configured low-cost acceptance model `alibaba/qwen3.5-flash`;
- the same exact three non-authorizing Authority Cut tools;
- external `ControlPlane.decide()` / revocation calls for human authority.

The adapter returns `foundation_model_invocation=PASS` only after all workflow state assertions pass. It never converts a provider response into a grant of authority.

## Public CI contract — PASS

Canonical CI run: `32220265475`.

Verified:

- `strands-agents[openai]==1.52.0` installs: **PASS**;
- `OpenAIModel` imports: **PASS**;
- gateway/model configuration contract: **PASS**;
- protected-preview health contract: **PASS**;
- missing runtime credential fails closed before provider/network execution: **PASS**;
- existing deterministic/live Strands proof remains **PASS**.

## Runtime acceptance attempt

A protected Vercel preview was first built successfully, but its SSO layer prevented the available connector from reaching the proof route. No application/model call occurred.

A separate transient gated acceptance project was then created to measure only the provider capability. Runtime diagnostics showed:

```text
has_ai_gateway_api_key = false
has_vercel_oidc_token = false
```

The gateway proof's credential guard therefore stopped execution before constructing a Gateway/model request.

Correct statuses:

- provider adapter: **PASS**;
- provider install/contract: **PASS**;
- actual foundation-model invocation: **UNRUN**;
- runtime blocker: **BLOCKED_RUNTIME_GATEWAY_CREDENTIAL**;
- request reached AI Gateway: **NO**;
- model spend reached Gateway: **NO**.

The transient model-call capability was immediately removed. The auxiliary project now exposes only a no-call receipt:

- receipt-only deployment: `dpl_DhThxgrR4R5wf2T79Ws2Da6poMwh`;
- model-call capability: `REMOVED`.

## Why this is not a submission blocker

The competition requires a Strands-based agent, not a specific external model provider. The accepted public Authority Cut path already executes the real Strands SDK Agent/tool loop and the full human-control workflow. Foundation-model execution would strengthen presentation/robustness evidence, but the current absence of a runtime Gateway credential is an optional score-upgrade boundary rather than an incomplete core implementation.

## Safe upgrade path

If a supported runtime credential is provisioned before submission:

1. deploy the protected acceptance entrypoint only;
2. confirm the credential exists without printing it;
3. run one full model-backed workflow;
4. accept PASS only if all tool-boundary and downstream-state assertions succeed;
5. retain only hashed model-response receipts in public evidence;
6. remove/disable the paid acceptance route again;
7. do not attach a cost-incurring model route to the public judge URL.

## Claim boundary

Do not claim a foundation model executed Authority Cut unless an actual provider invocation and all workflow assertions are observed. Current correct classification is **UNRUN / BLOCKED_RUNTIME_GATEWAY_CREDENTIAL**.
