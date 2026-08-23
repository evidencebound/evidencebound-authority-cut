# Authority Cut — AWS Capability Boundary

Snapshot updated: 2026-08-23

## Purpose

Keep separate two AWS facts that must not be conflated:

1. whether the new Authority Cut repository can reuse a pre-existing EvidenceBound GitHub OIDC role; and
2. whether Authority Cut itself can be deployed and invoked on Amazon Bedrock AgentCore Runtime through an independently authenticated owner path.

## Historical GitHub OIDC probe

A non-mutating GitHub Actions capability probe attempted to reuse a pre-existing EvidenceBound deployment role from the new repository identity `moneyparking/evidencebound-authority-cut`.

Canonical probe:

- GitHub Actions run: `32219855151`;
- operation: GitHub OIDC -> `sts:AssumeRoleWithWebIdentity`;
- result: **BLOCKED**;
- observed AWS error: `Not authorized to perform sts:AssumeRoleWithWebIdentity`.

Because authentication failed, the workflow intentionally stopped before any resource mutation or paid model request.

Correct historical statuses:

- reuse of the probed GitHub OIDC role: **BLOCKED_AWS_OIDC_TRUST**;
- Bedrock/foundation-model invocation through that probe: **UNRUN**;
- AgentCore creation/update through that probe: **UNRUN**.

This blocker was not rewritten as PASS.

## Verified owner-authenticated AgentCore path

On 2026-08-23 the project was deployed through authenticated AWS CloudShell using a dedicated least-privilege Runtime execution role.

Accepted configuration:

- region: `eu-central-1`;
- Runtime name: `AuthorityCutRuntime`;
- Runtime version: `1`;
- Runtime status: `READY`;
- direct-code S3 CodeZip;
- `PYTHON_3_13`;
- entry point `agentcore_main.py`;
- network mode `PUBLIC`;
- source HEAD packaged: `200d71f963bb4496a6f01a6cf1788695b3164739`;
- CodeZip SHA-256: `67c9ce7de97f48970d3c595e6914fef314011fa5cebccf4f01cd4b6bea32690e`.

A real `InvokeAgentRuntime` call returned HTTP 200 and the response passed all Authority Cut acceptance assertions:

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

Public documentation omits AWS account, role and bucket identifiers.

## Interpretation

The earlier GitHub OIDC denial was an identity/trust limitation of one deployment path, not a limitation of AgentCore or Authority Cut.

The accepted CloudShell deployment proves that the same Authority Cut Strands control semantics execute inside AgentCore Runtime without granting model-callable approve/revoke capabilities.

Correct current statuses:

- public Strands judge path: **PASS**;
- AgentCore Runtime deployment: **PASS**;
- AgentCore data-plane invocation: **PASS**;
- Strands loop inside AgentCore: **PASS**;
- foundation-model invocation: **UNVERIFIED**;
- historical reuse of pre-existing GitHub OIDC role: **BLOCKED_AWS_OIDC_TRUST**.

See `docs/agentcore-acceptance-2026-08-23.md`.