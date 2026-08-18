# Claims Ledger

| Claim | Evidence class | Status |
|---|---|---|
| 5 safe vendor-onboarding actions run before human attention | deterministic controlled workflow | VERIFIED locally |
| 7 protected effects map to 3 policy-defined decisions | static graph + evaluation | VERIFIED locally |
| 57.14% fewer prompts than per-protected-effect baseline in this fixed workflow | deterministic calculation `(7-3)/7` | VERIFIED locally |
| model-callable Strands tools cannot approve/revoke authority | source + unit test | VERIFIED locally |
| premature first-funds approval fails closed | unit/API test | VERIFIED locally |
| correction rolls back 6 executed reversible protected effects in controlled path | evaluation + HTTP smoke | VERIFIED locally |
| no irreversible transfer occurs without distinct `funds_release` authority in controlled path | tests/evaluation | VERIFIED locally |
| real Strands model executes the flow | real SDK/model run | UNVERIFIED / BLOCKED |
| AgentCore deployment works | live AWS evidence | UNVERIFIED / BLOCKED |
| public judge URL works | external deployment | UNVERIFIED / BLOCKED |
| mechanism improves real-world safety/productivity | field study | UNVERIFIED |
