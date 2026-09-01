# Authority Cut - Devpost Final Checklist

Snapshot updated: 2026-09-01

## Competition

**AWS Agents for Humans**

- target prize track: **Professional Agents**;
- public video: YouTube or Vimeo, maximum **5 minutes**;
- AWS Builder ID required;
- public source repository required;
- README + architecture documentation required;
- MIT or Apache license required - Authority Cut uses **Apache-2.0**;
- pre-existing work must be disclosed.

## Canonical submission links

Repository:

`https://github.com/evidencebound/evidencebound-authority-cut`

Public functional judge URL:

`https://evidencebound-authority-cut.vercel.app`

Video:

`https://youtu.be/dY8W-AP4mms`

Do not replace the existing video solely because the later Bedrock foundation-model acceptance passed.

## Engineering readiness

- Strands architecturally central: **PASS**
- real Strands SDK Agent loop: **PASS**
- real tool execution: **PASS**
- one deep professional workflow: **PASS**
- selective external human intervention boundary: **PASS**
- human correction changes downstream execution: **PASS**
- reversible recovery/compensation: **PASS**
- irreversible-effect gating: **PASS**
- provenance/receipts: **PASS**
- public repo: **PASS**
- public baseline CI: **PASS**
- public judge URL: **PASS**
- Apache-2.0 license: **PASS**
- pre-existing-work disclosure: **PASS**
- Amazon Bedrock AgentCore Runtime deployment: **PASS**
- AgentCore live invocation: **PASS**
- real Strands loop inside AgentCore: **PASS**
- native Amazon Bedrock / Nova Lite direct runtime invocation: **PASS**
- native Amazon Bedrock / Nova Lite full Strands Authority Cut execution: **PASS**

## Native Bedrock foundation-model acceptance

Verified 2026-09-01 at exact source SHA:

`9998565c6db8083446caef7e20a6cf03601533e6`

AWS target/readback:

- region: `eu-central-1`;
- inference profile: `eu.amazon.nova-lite-v1:0`;
- status: `ACTIVE`;
- type: `SYSTEM_DEFINED`;
- model count: 4.

Independent runtime probe:

```text
DIRECT_CONVERSE=PASS
STOP_REASON=end_turn
INPUT_TOKENS=8
OUTPUT_TOKENS=5
TOTAL_TOKENS=13
```

Full Strands result:

```text
AUTHORITY_CUT_BEDROCK=PASS
EXECUTION=REAL_STRANDS_AGENT_LOOP_FOUNDATION_MODEL
FOUNDATION_MODEL_INVOCATION=PASS
```

See `docs/bedrock-foundation-model-acceptance-2026-09-01.md`.

## Historical AgentCore acceptance

Verified 2026-08-23:

- region: `eu-central-1`;
- Runtime: `AuthorityCutRuntime`, version `1`;
- status: `READY`;
- direct-code / S3 CodeZip;
- Python: `PYTHON_3_13`;
- entry point: `agentcore_main.py`;
- packaged source HEAD: `200d71f963bb4496a6f01a6cf1788695b3164739`;
- CodeZip SHA-256: `67c9ce7de97f48970d3c595e6914fef314011fa5cebccf4f01cd4b6bea32690e`;
- `InvokeAgentRuntime`: HTTP 200;
- Strands loop inside AgentCore: PASS;
- `authority_mutation_tools=[]`: PASS;
- `authority_boundary=EXTERNAL_HUMAN_ONLY`: PASS;
- safe actions preserved: 5;
- reversible protected effects rolled back: 6;
- irreversible transmit: `INVALIDATED`.

Historical boundary: this AgentCore invocation used the deterministic custom Strands provider. Its old `FOUNDATION_MODEL_INVOCATION=UNVERIFIED` record remains correct for that invocation; the later native Bedrock acceptance is separate.

## Judge test path

1. Open `https://evidencebound-authority-cut.vercel.app`.
2. Select **Run live Strands judge path**.
3. Confirm the response identifies `REAL_STRANDS_AGENT_LOOP_DETERMINISTIC_MODEL`.
4. Confirm the published model-callable tools contain no approve/revoke function.
5. Confirm five safe actions execute before protected work.
6. Confirm `vendor-risk` is initially ready while future authorities are not ready.
7. Inspect the vendor-risk and payment-release phases.
8. Confirm `first-funds` becomes ready only after remittance preview while transmit remains blocked.
9. Inspect human correction: six protected reversible effects `ROLLED_BACK`, transmit `INVALIDATED`, five safe actions preserved.
10. Cross-check `/api/tool-boundary` and `/api/evaluation` if desired.
11. For AWS foundation-model proof, inspect `docs/bedrock-foundation-model-acceptance-2026-09-01.md`.
12. For AgentCore deployment evidence, inspect `docs/agentcore-acceptance-2026-08-23.md`.

## Stage Two judging mapping

### Technical Implementation

Lead with:

- authentic Strands execution;
- explicit external-human authority boundary;
- correction propagation;
- verified native Bedrock / Nova Lite foundation-model execution;
- verified AgentCore Runtime deployment/invocation;
- public CI and public judge path.

### Design

Show the decision surface: routine work is autonomous; only currently actionable semantic authority is escalated; future decisions remain not-ready until prerequisite evidence exists.

### Potential Impact

Describe professional operations use cases. Keep the 57.14% reduction explicitly scoped to the fixed vendor-onboarding workflow. Do not claim measured customer productivity.

### Creativity & Originality

Use the invention thesis **Authority Cut Sets + Reversible Correction Propagation**. Explicitly disclose overlap with existing HITL, interrupt/resume, delegated authorization, dependency invalidation and compensation patterns.

## Foundation-model truth boundary

Current status:

- native Amazon Bedrock / Nova Lite foundation-model invocation: **PASS**;
- full native Bedrock Strands Authority Cut workflow: **PASS**;
- historical optional Vercel AI Gateway provider contract: **PASS**;
- historical Vercel AI Gateway actual model request: **UNRUN**;
- public Vercel judge path: deterministic custom Strands provider;
- historical AgentCore run: deterministic custom Strands provider.

Do not infer that every deployment path is foundation-model-backed merely because the separate native Bedrock acceptance passed.

## Submission-safe update

If Devpost written fields remain editable without jeopardizing the submission state, add only the concise verified technical note from `handoff/BEDROCK_FOUNDATION_MODEL_ADDENDUM.md`.

Do not:

- replace the existing demo video;
- imply the existing video demonstrates the 2026-09-01 Bedrock acceptance;
- alter the public judge URL to require AWS credentials;
- weaken the external-human authority boundary.

## Historical AWS identity boundary

The pre-existing EvidenceBound GitHub OIDC role still does not trust this competition repository identity. That earlier probe remains `BLOCKED_AWS_OIDC_TRUST`.

Verified AWS acceptances used independently authenticated owner CloudShell paths rather than weakening that trust boundary.

## Final status

**READY engineering.**

Independent Devpost live submitted-state readback in this evidence pass: **UNRUN**.
