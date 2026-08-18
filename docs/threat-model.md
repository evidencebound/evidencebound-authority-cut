# Threat Model

## Authority boundary

The model may execute safe work, inspect the decision surface, and resume work using grants already recorded by the external principal. It cannot mint, approve, revoke or edit `HumanDecision` objects through the published Strands tool set.

## Threats addressed by the competition kernel

- protected tool call without current grant -> `BLOCKED`;
- denied bundle -> grants nothing;
- premature approval before prerequisite receipt exists -> rejected;
- attempt to collapse all authority into an invented mega-bundle -> impossible unless policy explicitly defines that bundle;
- human correction/revocation -> affected descendants invalidated;
- executed reversible affected effect -> compensation invoked;
- pending irreversible descendant -> invalidated/blocked rather than silently continued;
- unrelated safe work -> preserved;
- concurrent local state access -> serialized with explicit locks;
- API and Strands adapter split-brain within the process -> prevented by shared runtime singleton.

## Residual risks

- policy bundles can still be semantically wrong or over-broad;
- principal identity/authentication is not implemented in this local slice;
- process-local authority state is not distributed/durable;
- evidence references are bounded receipts, not independently authenticated external facts;
- real tool compensation can fail or be partial;
- irreversible effects cannot be undone by this mechanism;
- a compromised host/runtime can bypass application-level guarantees;
- real Strands and AgentCore behavior is unverified in the current offline environment.

## Minimality boundary

The Authority Cut is exact only over the **policy-defined candidate bundles**. This is deliberate: optimization is not allowed to enlarge consent scope merely to minimize interruptions.
