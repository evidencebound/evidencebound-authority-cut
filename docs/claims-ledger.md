# Claims Ledger

| Claim | Evidence class | Status |
|---|---|---|
| 5 safe vendor-onboarding actions run before human attention | deterministic controlled workflow + live public Strands path | VERIFIED |
| 7 protected effects map to 3 policy-defined decisions | static graph + evaluation | VERIFIED |
| 57.14% fewer prompts than per-protected-effect baseline in this fixed workflow | deterministic calculation `(7-3)/7` | VERIFIED |
| model-callable Strands tools cannot approve/revoke authority | source + tests + public CI + live Vercel tool boundary | VERIFIED |
| premature first-funds approval fails closed | unit/API tests + live authority surface | VERIFIED |
| first-funds becomes ready only after remittance preview exists | controlled/live workflow state | VERIFIED |
| correction rolls back 6 executed reversible protected effects in the fixed path | evaluation + public Strands loop + Vercel live proof + AgentCore invocation | VERIFIED |
| 5 unrelated safe actions remain executed after the correction | public Strands loop + Vercel live proof + AgentCore invocation | VERIFIED |
| pending irreversible transmit is invalidated after upstream correction | public Strands loop + Vercel live proof + AgentCore invocation | VERIFIED |
| no irreversible transfer occurs without distinct `funds_release` authority in controlled path | tests/evaluation/live proof | VERIFIED |
| dedicated public competition repository exists within submission period | repository provenance | VERIFIED |
| public GitHub Actions baseline test matrix passes | GitHub Actions | VERIFIED |
| `strands-agents==1.52.0` installs and `build_agent()` constructs the published Agent | public GitHub Actions Strands lane | VERIFIED |
| real Strands Agent loop executes all three published tools with deterministic custom Model provider | GitHub Actions + live Vercel runtime trace | VERIFIED |
| public judge URL executes the real Strands loop and returns the four-phase correction proof | Vercel production acceptance | VERIFIED |
| AgentCore direct-code entrypoint and adapter are present in the public source | source + contract tests | VERIFIED |
| AgentCore Runtime deployed from the accepted direct-code ZIP | AWS Runtime control-plane readback | VERIFIED |
| AgentCore Runtime reached `READY` in `eu-central-1` on Python 3.13 | AWS `GetAgentRuntime` readback | VERIFIED |
| real `InvokeAgentRuntime` returned HTTP 200 | AWS data-plane invocation | VERIFIED |
| real Strands SDK loop executed inside AgentCore Runtime | AgentCore response + assertions | VERIFIED |
| AgentCore invocation preserved `authority_mutation_tools=[]` and `EXTERNAL_HUMAN_ONLY` | AgentCore response + assertions | VERIFIED |
| AgentCore invocation preserved 5 safe actions, rolled back 6 reversible effects, and invalidated transmit | AgentCore response + assertions | VERIFIED |
| optional OpenAI-compatible foundation-model adapter installs and fails closed without runtime credential | public GitHub Actions gateway-contract lane | VERIFIED |
| a foundation-model-backed Strands agent executed the full workflow | external model invocation / trace | UNRUN / BLOCKED_RUNTIME_GATEWAY_CREDENTIAL |
| direct Vercel acceptance runtime had `AI_GATEWAY_API_KEY` | runtime boolean diagnostic | FALSE |
| direct Vercel acceptance runtime had `VERCEL_OIDC_TOKEN` | runtime boolean diagnostic | FALSE |
| model request reached Vercel AI Gateway during the acceptance attempt | fail-closed runtime diagnostic | NO |
| existing EvidenceBound AWS OIDC role can be assumed by this new repository identity | non-mutating GitHub OIDC probe | FALSE / BLOCKED_AWS_OIDC_TRUST |
| mechanism improves real-world safety/productivity | field study | UNVERIFIED |

## Canonical public production evidence

- URL: `https://evidencebound-authority-cut.vercel.app`
- Vercel project: `evidencebound-authority-cut`
- `/health`: HTTP 200
- `/api/strands-proof-get`: HTTP 200
- runtime log observed the real Strands tool sequence.

Canonical live proof returned:

- `execution=REAL_STRANDS_AGENT_LOOP_DETERMINISTIC_MODEL`
- `authority_mutation_tools=[]`
- `authority_boundary=EXTERNAL_HUMAN_ONLY`
- `safe_actions_preserved=5`
- `protected_reversible_effects_rolled_back=6`
- `irreversible_transmit_after_correction=INVALIDATED`
- `receipt_count=14`

## AgentCore acceptance evidence

Accepted 2026-08-23:

- region: `eu-central-1`;
- Runtime name: `AuthorityCutRuntime`;
- Runtime version: `1`;
- status: `READY`;
- direct-code S3 CodeZip;
- runtime: `PYTHON_3_13`;
- entry point: `agentcore_main.py`;
- source HEAD packaged: `200d71f963bb4496a6f01a6cf1788695b3164739`;
- CodeZip SHA-256: `67c9ce7de97f48970d3c595e6914fef314011fa5cebccf4f01cd4b6bea32690e`;
- `InvokeAgentRuntime`: HTTP 200;
- response assertions: AgentCore deployment PASS, live invocation PASS, Strands loop inside AgentCore PASS, external-human authority boundary PASS, safe actions preserved 5, reversible effects rolled back 6, irreversible transmit `INVALIDATED`.

AWS account, role and bucket identifiers are intentionally omitted from the public ledger.

See `docs/agentcore-acceptance-2026-08-23.md`.

## Foundation-model acceptance boundary

The optional adapter was not promoted to a public route. Its public-CI contract passed, but direct Vercel runtime diagnostics showed both supported Gateway credential sources absent. The acceptance function therefore failed before constructing a Gateway request.

Correct claim: **provider path prepared and fail-closed; actual foundation-model invocation UNRUN**.

## AWS identity boundary

Non-mutating GitHub Actions run `32219855151` attempted to reuse a pre-existing EvidenceBound deployment role from the new Authority Cut repository and received `Not authorized to perform sts:AssumeRoleWithWebIdentity`. That historical path remains blocked.

AgentCore was subsequently verified through an independently authenticated AWS CloudShell deployment path with a dedicated least-privilege Runtime execution role. The successful AgentCore acceptance does not retroactively convert the old GitHub OIDC probe into PASS.