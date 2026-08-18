# Claims Ledger

| Claim | Evidence class | Status |
|---|---|---|
| 5 safe vendor-onboarding actions run before human attention | deterministic controlled workflow | VERIFIED locally + public CI |
| 7 protected effects map to 3 policy-defined decisions | static graph + evaluation | VERIFIED locally + public CI |
| 57.14% fewer prompts than per-protected-effect baseline in this fixed workflow | deterministic calculation `(7-3)/7` | VERIFIED locally + public CI |
| model-callable Strands tools cannot approve/revoke authority | source + unit test + Strands construction lane | VERIFIED |
| premature first-funds approval fails closed | unit/API test | VERIFIED locally + public CI |
| correction rolls back 6 executed reversible protected effects in controlled path | evaluation + HTTP smoke | VERIFIED locally + public CI |
| no irreversible transfer occurs without distinct `funds_release` authority in controlled path | tests/evaluation | VERIFIED locally + public CI |
| dedicated public competition repository exists within submission period | repository provenance | VERIFIED |
| public GitHub Actions test matrix passes | GitHub Actions | VERIFIED |
| current `strands-agents` installs and `build_agent()` constructs an Agent | public GitHub Actions Strands lane | VERIFIED |
| a real Strands-supported model executes the full flow through the three tools | model invocation / trace | UNVERIFIED / BLOCKED |
| AgentCore deployment works | live AWS evidence | UNVERIFIED / BLOCKED |
| public judge URL works | external deployment | UNVERIFIED / BLOCKED |
| mechanism improves real-world safety/productivity | field study | UNVERIFIED |
