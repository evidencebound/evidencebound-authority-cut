# Claims Ledger

| Claim | Evidence class | Status |
|---|---|---|
| 5 safe vendor-onboarding actions run before human attention | deterministic controlled workflow + live public Strands path | VERIFIED |
| 7 protected effects map to 3 policy-defined decisions | static graph + evaluation | VERIFIED |
| 57.14% fewer prompts than per-protected-effect baseline in this fixed workflow | deterministic calculation `(7-3)/7` | VERIFIED |
| model-callable Strands tools cannot approve/revoke authority | source + tests + public CI + live Vercel tool boundary | VERIFIED |
| premature first-funds approval fails closed | unit/API tests + live authority surface | VERIFIED |
| first-funds becomes ready only after remittance preview exists | controlled/live workflow state | VERIFIED |
| correction rolls back 6 executed reversible protected effects in the fixed path | evaluation + public Strands loop + Vercel live proof | VERIFIED |
| 5 unrelated safe actions remain executed after the correction | public Strands loop + Vercel live proof | VERIFIED |
| pending irreversible transmit is invalidated after upstream correction | public Strands loop + Vercel live proof | VERIFIED |
| no irreversible transfer occurs without distinct `funds_release` authority in controlled path | tests/evaluation/live proof | VERIFIED |
| dedicated public competition repository exists within submission period | repository provenance | VERIFIED |
| public GitHub Actions test matrix passes | GitHub Actions | VERIFIED |
| `strands-agents==1.52.0` installs and `build_agent()` constructs the published Agent | public GitHub Actions Strands lane | VERIFIED |
| real Strands Agent loop executes all three published tools with deterministic custom Model provider | GitHub Actions + live Vercel runtime trace | VERIFIED |
| public judge URL executes the real Strands loop and returns the four-phase correction proof | Vercel production acceptance | VERIFIED |
| optional OpenAI-compatible foundation-model adapter installs and fails closed without runtime credential | public GitHub Actions gateway-contract lane | VERIFIED |
| a foundation-model-backed Strands agent executed the full workflow | external model invocation / trace | UNRUN / BLOCKED_RUNTIME_GATEWAY_CREDENTIAL |
| direct Vercel acceptance runtime had `AI_GATEWAY_API_KEY` | runtime boolean diagnostic | FALSE |
| direct Vercel acceptance runtime had `VERCEL_OIDC_TOKEN` | runtime boolean diagnostic | FALSE |
| model request reached Vercel AI Gateway during the acceptance attempt | fail-closed runtime diagnostic | NO |
| existing EvidenceBound AWS OIDC role can be assumed by this new repository identity | non-mutating GitHub OIDC probe | FALSE / BLOCKED_AWS_OIDC_TRUST |
| Bedrock/AgentCore resource mutation occurred during the OIDC probe | workflow boundary | UNRUN |
| AgentCore deployment works | live AWS evidence | UNRUN / BLOCKED_AWS_OIDC_TRUST |
| mechanism improves real-world safety/productivity | field study | UNVERIFIED |

## Canonical public production evidence

- URL: `https://evidencebound-authority-cut.vercel.app`
- Vercel project: `evidencebound-authority-cut`
- project ID: `prj_WPX42JQ08alE6WfuqlS0xA8XpBzT`
- canonical source commit: `1cf640d735d822f3a66c517e5eeb8711fec2a040`
- accepted deployment: `dpl_8b5jXwdhD57u2b4XfvWNRJSLsrey`
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

## Foundation-model acceptance boundary

The optional adapter was not promoted to a public route. Its public-CI contract passed, but direct Vercel runtime diagnostics showed both supported Gateway credential sources absent. The acceptance function therefore failed before constructing a Gateway request. The transient model-call route was removed and the auxiliary project now exposes only a no-call receipt.

Correct claim: **provider path prepared and fail-closed; actual foundation-model invocation UNRUN**.

## AWS capability boundary

Non-mutating GitHub Actions run `32219855151` attempted the existing EvidenceBound deployment role from the new Authority Cut repository and received `Not authorized to perform sts:AssumeRoleWithWebIdentity`. No Bedrock model discovery, paid model invocation, AgentCore creation or other AWS resource mutation followed that denial.

Correct claim: **AgentCore is an optional score upgrade blocked by repository IAM trust, not a completed integration**.
