# AgentCore Decision

AgentCore is advantageous for the final judge path because Runtime/Identity/Observability can strengthen deployment reliability and the Technical Implementation criterion. It is not required for the deterministic control primitive itself.

## Current verified state

- dedicated public competition repository: **PASS**;
- public GitHub Actions: **PASS**;
- real `strands-agents` package installation: **PASS** in public CI;
- Strands `Agent` construction with the three non-authorizing tools: **PASS**;
- real Strands-supported model invocation through the end-to-end workflow: **BLOCKED / UNVERIFIED**;
- AgentCore deployment: **BLOCKED / UNVERIFIED**.

## Deployment decision

Do not use AgentCore merely for a logo/infrastructure checkbox. First pass the real Strands model-invocation gate while preserving external human authority. Then deploy the same accepted control boundary to AgentCore if Runtime, Identity and Observability materially improve the live judge path.

This workspace has no authenticated AWS competition deployment context or AgentCore deployment connector/credentials. Do not claim AgentCore usage until a real runtime is deployed, the exact source revision is known, and the external judge workflow is smoke-tested.

Rollback principle: retain a non-AgentCore local/reference execution path until live AgentCore acceptance passes, so deployment integration cannot invalidate the core competition evidence.
