# AgentCore Decision

## Decision

Amazon Bedrock AgentCore is a **non-blocking Technical Implementation score upgrade**, not a completion requirement for Authority Cut.

The competition's required Strands-centered professional agent path is already implemented and publicly executable. The canonical judge service runs the real Strands SDK Agent/tool loop, preserves the external-human-only authority boundary, propagates correction through reversible descendants, and gates the irreversible transfer.

AgentCore would still be valuable because Runtime, Identity and Observability could strengthen deployment reliability, principal identity and judge traceability. It must not be added merely as an infrastructure checkbox or in a way that weakens the control boundary.

## Current verified state

- dedicated public competition repository: **PASS**;
- public GitHub Actions: **PASS**;
- `strands-agents==1.52.0` installation: **PASS**;
- published Strands `Agent` construction: **PASS**;
- real Strands Agent/tool loop: **PASS** in CI and live public Vercel production;
- exact three non-authorizing model tools: **PASS**;
- public judge endpoint: **PASS**;
- correction propagation / reversible compensation: **PASS**;
- optional OpenAI-compatible foundation-model provider contract: **PASS**;
- actual foundation-model execution: **UNRUN / BLOCKED_RUNTIME_GATEWAY_CREDENTIAL**;
- AgentCore authenticated deployment: **UNRUN / BLOCKED_AWS_OIDC_TRUST**.

## Exact AWS capability blocker

A non-mutating GitHub Actions capability probe attempted the pre-existing EvidenceBound deployment role candidate:

`arn:aws:iam::877348951762:role/EvidenceBoundGitHubDeployRole`

Canonical probe:

- workflow run: `32219855151`;
- repository: `moneyparking/evidencebound-authority-cut`;
- operation attempted: GitHub OIDC -> `sts:AssumeRoleWithWebIdentity` only;
- result: **BLOCKED** — `Not authorized to perform sts:AssumeRoleWithWebIdentity`;
- Bedrock model discovery: **UNRUN**;
- paid model invocation: **UNRUN**;
- AgentCore creation/update: **UNRUN**;
- any other AWS resource mutation: **UNRUN**.

The probe PR was closed without merge after the boundary was measured, so the public `main` does not contain a workflow that repeatedly attempts the blocked role.

## Owner-enabled upgrade path

If AgentCore is pursued before submission, the safe sequence is:

1. create a **dedicated least-privilege GitHub OIDC role** for `moneyparking/evidencebound-authority-cut`, or explicitly extend a suitable role's trust policy to this new repository/ref;
2. grant only the AgentCore/Bedrock permissions required by the selected Runtime/Identity/Observability path;
3. verify `sts:GetCallerIdentity` from this repository before any resource mutation;
4. deploy the exact accepted Authority Cut source revision to AgentCore;
5. invoke the same vendor-onboarding judge workflow;
6. verify the external human authority channel remains outside the model tool set;
7. capture AgentCore Runtime/Identity/Observability evidence only after live acceptance;
8. retain the current public Vercel path as rollback/reference until AgentCore acceptance is complete.

Do not reuse the old role by assumption. The capability probe has already shown that the new repository identity is not currently authorized.

## Kill / rollback criteria

Do not add AgentCore if it:

- requires weakening the external-human authority boundary;
- cannot be deployed and smoke-tested before submission;
- obscures the distinction between pre-existing EvidenceBound work and this new competition implementation;
- introduces an unstable judge dependency without enough judging upside.

Rollback remains the current public Strands judge service at `https://evidencebound-authority-cut.vercel.app`.
