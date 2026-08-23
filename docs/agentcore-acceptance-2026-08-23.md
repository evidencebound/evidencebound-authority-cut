# AgentCore Runtime Acceptance — 2026-08-23

## Decision

Amazon Bedrock AgentCore Runtime is now **VERIFIED** for Authority Cut.

This acceptance deployed the competition-period Authority Cut source as a direct-code ZIP to Amazon Bedrock AgentCore Runtime in `eu-central-1` and invoked the runtime through the AgentCore data plane. The runtime executed the same real Strands SDK Agent/tool proof used by the public judge path.

## Deployment evidence

- region: `eu-central-1` (Frankfurt)
- AgentCore Runtime name: `AuthorityCutRuntime`
- runtime version: `1`
- runtime status: `READY`
- deployment mode: direct code / S3 CodeZip
- runtime: `PYTHON_3_13`
- entry point: `agentcore_main.py`
- network mode: `PUBLIC`
- lifecycle: idle session timeout 300 seconds; max lifetime 1800 seconds
- CodeZip SHA-256: `67c9ce7de97f48970d3c595e6914fef314011fa5cebccf4f01cd4b6bea32690e`
- deployed source HEAD before packaging: `200d71f963bb4496a6f01a6cf1788695b3164739`

AWS account identifiers, role ARN and S3 bucket identifiers are intentionally omitted from this public evidence file.

## Live invocation evidence

`InvokeAgentRuntime` returned HTTP status **200** and the runtime response passed all acceptance assertions:

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

The accepted response included:

```text
execution = REAL_STRANDS_AGENT_LOOP_DETERMINISTIC_MODEL
agentcore = RUNTIME_ADAPTER_EXECUTED
agentcore_runtime_adapter = BEDROCK_AGENTCORE_DIRECT_CODE
authority_mutation_tools = []
authority_boundary = EXTERNAL_HUMAN_ONLY
safe_actions_preserved = 5
protected_reversible_effects_rolled_back = 6
irreversible_transmit_after_correction = INVALIDATED
receipt_count = 14
```

## What this proves

The accepted AgentCore Runtime invocation proves that:

1. the deployed AgentCore entry point loads successfully under Python 3.13;
2. AgentCore Runtime executes the Authority Cut adapter;
3. the adapter executes the real Strands SDK Agent/tool loop;
4. the deployed model-callable tool surface still contains no authority-mutation tool;
5. five unrelated safe actions remain executed after the correction;
6. six executed reversible protected descendants are compensated;
7. the pending irreversible transmit action becomes `INVALIDATED`;
8. the foundation-model boundary remains explicit.

## What this does not prove

This acceptance does **not** prove:

- foundation-model-backed execution;
- correctness of arbitrary enterprise policy;
- authenticated end-user principal identity;
- durable distributed authority state;
- safe compensation against arbitrary external vendor/payment systems;
- generalized productivity or safety improvement.

The AgentCore runtime uses the same deterministic custom Strands `Model` provider as the public proof. `FOUNDATION_MODEL_INVOCATION=UNVERIFIED` remains the correct status.

## Historical blocker

An earlier GitHub OIDC probe was blocked because the pre-existing EvidenceBound deployment role did not trust the new competition repository identity. That historical result remains valid for that role/repository path. It was **not** fixed or reclassified as PASS.

The verified AgentCore deployment used an owner-authenticated AWS CloudShell path with a dedicated least-privilege runtime execution role, avoiding any need to weaken the prior OIDC boundary.
