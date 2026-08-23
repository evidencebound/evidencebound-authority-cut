# Authority Cut - Devpost Final Checklist

Snapshot updated: 2026-08-23

## Competition

**AWS Agents for Humans**

- submission deadline: **2026-09-14 17:00 PT / 2026-09-15 00:00 UTC**;
- target prize track: **Professional Agents**;
- public video: YouTube or Vimeo, maximum **5 minutes**;
- AWS Builder ID required;
- public source repository required;
- README + architecture documentation required;
- MIT or Apache license required - Authority Cut uses **Apache-2.0**;
- pre-existing work must be disclosed.

## Canonical submission links

Repository:

`https://github.com/moneyparking/evidencebound-authority-cut`

Public functional judge URL:

`https://evidencebound-authority-cut.vercel.app`

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
- foundation-model execution: **UNVERIFIED / optional**

## AgentCore acceptance

Verified 2026-08-23:

- region: `eu-central-1`
- Runtime: `AuthorityCutRuntime`, version `1`
- status: `READY`
- direct-code / S3 CodeZip
- Python: `PYTHON_3_13`
- entry point: `agentcore_main.py`
- packaged source HEAD: `200d71f963bb4496a6f01a6cf1788695b3164739`
- CodeZip SHA-256: `67c9ce7de97f48970d3c595e6914fef314011fa5cebccf4f01cd4b6bea32690e`
- `InvokeAgentRuntime`: HTTP 200
- Strands loop inside AgentCore: PASS
- `authority_mutation_tools=[]`: PASS
- `authority_boundary=EXTERNAL_HUMAN_ONLY`: PASS
- safe actions preserved: 5
- reversible protected effects rolled back: 6
- irreversible transmit: `INVALIDATED`
- foundation-model invocation: `UNVERIFIED`

See `docs/agentcore-acceptance-2026-08-23.md`.

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
11. For AWS deployment evidence, inspect `docs/agentcore-acceptance-2026-08-23.md`.

## Stage Two judging mapping

### Technical Implementation

Lead with:

- authentic Strands execution;
- explicit external-human authority boundary;
- correction propagation;
- verified AgentCore Runtime deployment/invocation;
- public CI and public judge path.

Do not imply that AgentCore acceptance proves foundation-model execution.

### Design

Show the decision surface: routine work is autonomous; only currently actionable semantic authority is escalated; future decisions remain not-ready until prerequisite evidence exists.

### Potential Impact

Describe professional operations use cases. Keep the 57.14% reduction explicitly scoped to the fixed vendor-onboarding workflow. Do not claim measured customer productivity.

### Creativity & Originality

Use the invention thesis **Authority Cut Sets + Reversible Correction Propagation**. Explicitly disclose overlap with existing HITL, interrupt/resume, delegated authorization, dependency invalidation and compensation patterns.

### Presentation

Show real working execution. The final video should include the recorded click on **Run live Strands judge path** and the returned live states. Include AgentCore verification briefly as production-depth evidence, not as the main story.

## Video checklist

- [x] Problem statement: too many interruptions vs silent authority accumulation.
- [x] Who it is for: procurement / finance / compliance / operations.
- [x] Strands tool boundary explained.
- [x] Fixed-workflow evaluation explained.
- [x] Matthew narration produced.
- [x] Real public live Strands capture recorded.
- [x] Verified AgentCore Runtime acceptance obtained.
- [ ] Final edit embeds the real live Strands capture.
- [ ] Final edit includes a concise verified AgentCore proof segment.
- [ ] Final edit states `FOUNDATION_MODEL_INVOCATION=UNVERIFIED`.
- [ ] Final published video <=5 minutes.
- [ ] Video published **Public** on YouTube/Vimeo.

## Form / identity actions

- [x] Hackathon registration completed.
- [x] AWS Builder ID available.
- [x] Devpost project shell `Authority Cut` exists.
- [x] Project description / built-with / repo / live judge link prepared.
- [ ] Upload final architecture diagram in the required Devpost field.
- [ ] Add final public video URL.
- [ ] Ensure Professional Agents is selected.
- [ ] Include pre-existing-work disclosure.
- [ ] Read back all written claims against `docs/claims-ledger.md` and `AWS_JUDGE_PACK.md`.
- [ ] Submit.
- [ ] Live submitted readback.

## Foundation-model boundary

Current status:

- provider adapter/contract: **PASS**;
- actual foundation-model invocation: **UNVERIFIED / UNRUN**.

The accepted AgentCore deployment uses the deterministic custom Strands `Model` provider. Do not add a foundation-model claim merely because AgentCore is now verified.

## Historical AWS identity boundary

The pre-existing EvidenceBound GitHub OIDC role still does not trust this competition repository identity. That earlier probe remains `BLOCKED_AWS_OIDC_TRUST`.

The verified AgentCore Runtime was deployed through an independently authenticated owner CloudShell path with a dedicated least-privilege Runtime role.

## builder.aws bonus

Three technically substantive draft posts already exist in `handoff/BUILDER_AWS_BONUS_POSTS.md`.

If the current bonus remains available under the final rules readback, publish up to three qualifying posts only after the main submission package is stable. Do not delay required submission work for bonus content.

## Final status

**READY engineering / NOT YET SUBMITTED.**

Remaining critical path:

1. final video edit with live Strands + concise AgentCore evidence;
2. publish video Public;
3. upload architecture file;
4. final Devpost write/readback;
5. submit and verify `submitted` state.