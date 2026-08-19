# Authority Cut — AWS Capability Boundary

Snapshot: 2026-08-19

## Purpose

Measure whether the new Authority Cut repository can reuse an existing EvidenceBound GitHub OIDC deployment role **without mutating AWS resources or making paid model calls**.

## Candidate identity

- AWS account: `877348951762`
- candidate role: `arn:aws:iam::877348951762:role/EvidenceBoundGitHubDeployRole`
- repository identity under test: `moneyparking/evidencebound-authority-cut`

The role ARN is deployment metadata, not a secret.

## Canonical probe

- GitHub Actions run: `32219855151`
- operation: GitHub OIDC -> `sts:AssumeRoleWithWebIdentity`
- retry attempts capped to 3 in the final probe revision
- result: **BLOCKED**
- observed AWS error class/message: `Not authorized to perform sts:AssumeRoleWithWebIdentity`

Because STS authentication failed, the workflow deliberately did not continue to any AWS capability that might create cost or mutate infrastructure.

## Exact downstream statuses

- STS role assumption: **BLOCKED_AWS_OIDC_TRUST**
- `sts:GetCallerIdentity`: **UNRUN**
- Bedrock model discovery: **UNRUN**
- Bedrock/foundation-model invocation: **UNRUN**
- AgentCore Runtime creation: **UNRUN**
- AgentCore Identity/Observability setup: **UNRUN**
- CloudFormation/resource mutation: **UNRUN**
- paid AWS operation intentionally initiated by the probe: **UNRUN**

The probe PR was closed without merge after the capability boundary was measured, so the public `main` is not burdened with a repeatedly failing AWS workflow.

## Interpretation

This is not a failure of Authority Cut or Strands. It is an external deployment-identity boundary: the new competition repository is not authorized by the probed role's trust configuration.

Do not infer that the old EvidenceBound deployment role is reusable simply because it exists in the same AWS account.

## Owner action for optional AgentCore upgrade

If AgentCore is pursued before submission:

1. create a dedicated least-privilege GitHub OIDC role for this repository, or explicitly extend an appropriate role's trust policy to `moneyparking/evidencebound-authority-cut` and the intended ref/environment;
2. verify `sts:GetCallerIdentity` from this repository first;
3. grant only the required Bedrock AgentCore Runtime/Identity/Observability and model permissions;
4. deploy the exact accepted public source revision;
5. run the complete vendor-onboarding live judge path;
6. preserve the external-human approve/revoke boundary;
7. capture AgentCore evidence only after live acceptance.

## Submission classification

AgentCore is an **optional score upgrade** and currently **BLOCKED_AWS_OIDC_TRUST**. The project itself remains READY through the accepted public Strands execution path.
