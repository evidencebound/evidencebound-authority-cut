# AgentCore Decision

## Decision

Amazon Bedrock AgentCore is now a **verified Technical Implementation score upgrade** for Authority Cut.

The required Strands-centered professional-agent path remains independently public and executable on the canonical judge surface. AgentCore was added only after that path was accepted, and the integration preserves the exact same external-human authority boundary rather than changing the project semantics to satisfy an infrastructure checkbox.

## Current verified state

- dedicated public competition repository: **PASS**;
- public GitHub Actions baseline: **PASS**;
- `strands-agents==1.52.0` installation: **PASS**;
- published Strands `Agent` construction: **PASS**;
- real Strands Agent/tool loop: **PASS** in CI and live public Vercel production;
- exact three non-authorizing model tools: **PASS**;
- public judge endpoint: **PASS**;
- correction propagation / reversible compensation: **PASS**;
- optional OpenAI-compatible foundation-model provider contract: **PASS**;
- actual foundation-model execution: **UNRUN / BLOCKED_RUNTIME_GATEWAY_CREDENTIAL**;
- AgentCore direct-code adapter contract: **PASS**;
- AgentCore Runtime deployment: **PASS**;
- AgentCore live invocation: **PASS**;
- real Strands loop inside AgentCore: **PASS**.

## Accepted AgentCore configuration

- region: `eu-central-1` (Frankfurt)
- Runtime name: `AuthorityCutRuntime`
- Runtime version: `1`
- status: `READY`
- deployment mode: direct code / S3 CodeZip
- runtime: `PYTHON_3_13`
- entry point: `agentcore_main.py`
- network mode: `PUBLIC`
- packaged source HEAD: `200d71f963bb4496a6f01a6cf1788695b3164739`
- CodeZip SHA-256: `67c9ce7de97f48970d3c595e6914fef314011fa5cebccf4f01cd4b6bea32690e`

Public evidence intentionally omits AWS account, role and bucket identifiers.

## Acceptance assertions

A real AgentCore `InvokeAgentRuntime` call returned HTTP 200. The response passed:

```text
AGENTCORE_RUNTIME_DEPLOYMENT=PASS
AGENTCORE_LIVE_INVOCATION=PASS
STRANDS_LOOP_INSIDE_AGENTCORE=PASS
HUMAN_AUTHORITY_BOUNDARY=PASS
SAFE_ACTIONS_PRESERVED=5
REVERSIBLE_EFFECTS_ROLLED_BACK=6
IRREVERSIBLE_TRANSMIT=INVALIDATED
FOUNDATION_MODEL_INVOCATION=UNVERIFIED
```

The runtime response retained:

- `execution=REAL_STRANDS_AGENT_LOOP_DETERMINISTIC_MODEL`;
- `authority_mutation_tools=[]`;
- `authority_boundary=EXTERNAL_HUMAN_ONLY`;
- five safe actions preserved;
- six reversible protected effects rolled back;
- pending irreversible transmit invalidated;
- 14 receipts.

See `docs/agentcore-acceptance-2026-08-23.md`.

## Historical GitHub OIDC boundary

The earlier non-mutating GitHub OIDC probe remains a valid historical result:

- repository path attempted to reuse a pre-existing EvidenceBound deployment role;
- `sts:AssumeRoleWithWebIdentity`: **BLOCKED**;
- no AgentCore/resource mutation followed that denial.

That role trust was not silently reclassified as working. The successful AgentCore deployment used an owner-authenticated AWS CloudShell path with a dedicated least-privilege execution role.

## Foundation-model boundary

The accepted AgentCore Runtime uses the same deterministic custom Strands `Model` provider as the public reproducible judge proof. Therefore:

- AgentCore infrastructure execution: **PASS**;
- Strands orchestration inside AgentCore: **PASS**;
- foundation-model invocation: **UNVERIFIED**.

Do not infer foundation-model quality or Bedrock model execution from AgentCore acceptance.

## Rollback

The canonical public Vercel judge path remains the stable zero-credential public fallback/reference at:

`https://evidencebound-authority-cut.vercel.app`

AgentCore is a verified deployment surface, not a reason to make the public judge experience depend on AWS credentials.