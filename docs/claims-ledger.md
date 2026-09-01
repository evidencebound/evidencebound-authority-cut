# Claims Ledger

| Claim | Evidence class | Status |
|---|---|---|
| 5 safe vendor-onboarding actions run before human attention | deterministic controlled workflow + live public Strands path + native Bedrock acceptance | VERIFIED |
| 7 protected effects map to 3 policy-defined decisions | static graph + evaluation | VERIFIED |
| 57.14% fewer prompts than per-protected-effect baseline in this fixed workflow | deterministic calculation `(7-3)/7` | VERIFIED |
| model-callable Strands tools cannot approve/revoke authority | source + tests + public CI + live Vercel tool boundary + native Bedrock acceptance | VERIFIED |
| premature first-funds approval fails closed | unit/API tests + live authority surface | VERIFIED |
| first-funds becomes ready only after remittance preview exists | controlled/live workflow state + native Bedrock acceptance | VERIFIED |
| correction rolls back 6 executed reversible protected effects in the fixed path | evaluation + public Strands loop + Vercel live proof + AgentCore invocation + native Bedrock acceptance | VERIFIED |
| 5 unrelated safe actions remain executed after the correction | public Strands loop + Vercel live proof + AgentCore invocation + native Bedrock acceptance | VERIFIED |
| pending irreversible transmit is invalidated after upstream correction | public Strands loop + Vercel live proof + AgentCore invocation + native Bedrock acceptance | VERIFIED |
| no irreversible transfer occurs without distinct `funds_release` authority in controlled path | tests/evaluation/live proof + native Bedrock acceptance | VERIFIED |
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
| native Amazon Bedrock inference profile `eu.amazon.nova-lite-v1:0` was ACTIVE in `eu-central-1` | owner-authenticated AWS CloudShell control-plane readback | VERIFIED |
| direct Amazon Bedrock Runtime `Converse` invocation against Nova Lite succeeded | owner-authenticated AWS CloudShell runtime probe; token usage observed | VERIFIED |
| a real Amazon Nova Lite foundation-model-backed Strands agent executed the Authority Cut workflow | native Bedrock acceptance at exact source SHA; fail-closed response-receipt and workflow assertions | VERIFIED |
| native Bedrock foundation-model run preserved the external-human-only authority boundary | exact three-tool source + live model sequence + fail-closed promotion gate | VERIFIED |
| optional OpenAI-compatible foundation-model adapter installs and fails closed without runtime credential | public GitHub Actions gateway-contract lane | VERIFIED |
| historical Vercel AI Gateway foundation-model invocation occurred | fail-closed runtime diagnostic | NO / UNRUN |
| direct Vercel acceptance runtime had `AI_GATEWAY_API_KEY` | runtime boolean diagnostic | FALSE |
| direct Vercel acceptance runtime had `VERCEL_OIDC_TOKEN` | runtime boolean diagnostic | FALSE |
| existing EvidenceBound AWS OIDC role can be assumed by this new repository identity | non-mutating GitHub OIDC probe | FALSE / BLOCKED_AWS_OIDC_TRUST |
| Devpost Authority Cut project remains published after Bedrock evidence update | authenticated Devpost project readback | VERIFIED |
| Agents for Humans submission remains submitted after project description update | authenticated Devpost project + hackathon relationship readback | VERIFIED |
| existing demo video remains `https://youtu.be/dY8W-AP4mms` after Devpost update | authenticated Devpost project readback | VERIFIED |
| mechanism improves real-world safety/productivity | field study | UNVERIFIED |

## Canonical public production evidence

- URL: `https://evidencebound-authority-cut.vercel.app`
- Vercel project: `evidencebound-authority-cut`
- `/health`: HTTP 200
- `/api/strands-proof-get`: HTTP 200
- runtime log observed the real Strands tool sequence.

Canonical public live proof remains intentionally deterministic and credential-free:

- `execution=REAL_STRANDS_AGENT_LOOP_DETERMINISTIC_MODEL`
- `authority_mutation_tools=[]`
- `authority_boundary=EXTERNAL_HUMAN_ONLY`
- `safe_actions_preserved=5`
- `protected_reversible_effects_rolled_back=6`
- `irreversible_transmit_after_correction=INVALIDATED`
- `receipt_count=14`

## Native Amazon Bedrock foundation-model acceptance

Accepted 2026-09-01 from owner-authenticated AWS CloudShell at exact Authority Cut source SHA:

`9998565c6db8083446caef7e20a6cf03601533e6`

AWS preflight:

- identity: PASS;
- region: `eu-central-1`;
- inference profile: `eu.amazon.nova-lite-v1:0`;
- profile status: `ACTIVE`;
- profile type: `SYSTEM_DEFINED`;
- profile target-model count: `4`.

Independent direct runtime probe:

```text
DIRECT_CONVERSE=PASS
STOP_REASON=end_turn
INPUT_TOKENS=8
OUTPUT_TOKENS=5
TOTAL_TOKENS=13
```

Full Strands / Authority Cut run:

```text
AUTHORITY_CUT_BEDROCK=PASS
EXECUTION=REAL_STRANDS_AGENT_LOOP_FOUNDATION_MODEL
FOUNDATION_MODEL_INVOCATION=PASS
```

The accepted code can promote this status only after three distinct model-response SHA-256 receipts with positive token usage and all Authority Cut control/correction invariants pass. Approve/revoke remains outside the model-callable tool set.

See `docs/bedrock-foundation-model-acceptance-2026-09-01.md`.

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

The historical AgentCore deployment used the deterministic custom Strands provider. The separate 2026-09-01 native Bedrock acceptance does not retroactively change that historical fact.

See `docs/agentcore-acceptance-2026-08-23.md`.

## Foundation-model acceptance boundary

Two provider paths must remain distinguished:

1. **Native Amazon Bedrock / Nova Lite:** real runtime invocation and full Strands Authority Cut acceptance **VERIFIED / PASS** on 2026-09-01.
2. **Historical optional Vercel AI Gateway adapter:** provider contract **PASS**, actual Gateway model request **UNRUN** because the runtime credential was absent.

The canonical public Vercel judge surface remains the deterministic custom Strands provider. A paid model endpoint was not added to that public route.

## Devpost submission readback

Authenticated 2026-09-01 readback after the Bedrock evidence update verified:

- project id: `1394239`;
- slug: `authority-cut`;
- state: `published`;
- URL: `https://devpost.com/software/authority-cut`;
- video unchanged: `https://youtu.be/dY8W-AP4mms`;
- hackathon: `Agents for Humans Hackathon` / `agentsforhumans`;
- `submitted_at`: `2026-08-23T05:14:52.895-04:00`;
- authenticated hackathon relationships: `registered`, `submitted`;
- live description contains the native Bedrock PASS evidence while preserving the deterministic-public-proof, historical AgentCore, historical Gateway and OIDC truth boundaries.

No re-submission, video replacement or judge-URL change was required.

## AWS identity boundary

Non-mutating GitHub Actions run `32219855151` attempted to reuse a pre-existing EvidenceBound deployment role from the new Authority Cut repository and received `Not authorized to perform sts:AssumeRoleWithWebIdentity`. That historical path remains blocked.

AgentCore was subsequently verified through an independently authenticated AWS CloudShell deployment path with a dedicated least-privilege Runtime execution role. The native Bedrock foundation-model acceptance was also executed through owner-authenticated AWS CloudShell. Neither result retroactively converts the old GitHub OIDC probe into PASS.
