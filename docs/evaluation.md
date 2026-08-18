# Controlled Evaluation

## Fixed vendor-onboarding workflow

| Property | Observed controlled result |
|---|---:|
| Safe actions before human attention | 5 |
| Protected tool effects | 7 |
| Per-protected-effect HITL baseline prompts | 7 |
| Policy-defined Authority Cut decisions | 3 |
| Prompt reduction in this fixed workflow | 57.14% |
| Reversible protected effects executed before correction | 6 |
| Reversible protected effects rolled back after correction | 6 |
| Irreversible effects executed without `funds_release` | 0 |
| Unaffected safe actions preserved | 5 |

Run:

```bash
PYTHONPATH=src python scripts/run_evaluation.py
```

The retained result is `results/evaluation.json`.

## Properties covered by tests

1. safe work proceeds without human interruption;
2. the model-callable Strands tool set cannot approve or revoke authority;
3. denied decisions grant nothing;
4. the decision surface is an exact minimum cover over **policy-defined** bundles;
5. uncovered authority fails closed;
6. future authority may be visible without being prematurely approvable;
7. `first-funds` binds the actual remittance prerequisite receipt;
8. corrections invalidate affected descendants and preserve unrelated work;
9. reversible executed effects are compensated;
10. irreversible effects are never falsely labelled rolled back;
11. API and Strands adapter observe the same shared runtime state;
12. local HTTP judge path fails closed on premature irreversible approval.

## Evidence class

All current measurements are deterministic competition-period mechanism evidence. They do **not** establish human-time savings across organizations, model robustness, real vendor-system compensation reliability, real Strands execution, or AgentCore production behavior.

## External acceptance still required

- networked install of current `strands-agents`;
- real Strands model invocation through the three-tool boundary;
- adversarial prompt attempts to self-approve/bypass authority;
- public repository CI;
- AWS deployment and external judge smoke;
- AgentCore Runtime/Identity/Observability if the integration increases score without weakening the authority boundary.
