# Architecture

Authority Cut is presented as a bank vendor-onboarding product first: the Strands agent handles routine work, BANK-ECP-style evidence determines whether the risky decision is supportable, a human supplies consequential authority, and a later evidence correction can invalidate stale authority and selectively undo affected work.

```text
Bank vendor-onboarding goal
          |
          v
     Strands Agent
          |
          | model-callable operational tools only
          v
   Shared ControlPlane <---------------- External Human Principal
          ^                                  | approve / deny / revoke
          |                                  |
          |                           Human Authority API
          |
          +---------------------- External evidence update
          |                             (non-model channel)
          |
  BANK-ECP evidence gate
  PASS / HOLD / ABSTAIN
          |
          v
  policy + execution state
          |
          +--> safe routine work
          |
          +--> protected vendor setup when human authority is valid
          |
          +--> evidence PASS → HOLD invalidates stale authority
                       |
                       +--> compensate affected reversible descendants
                       +--> preserve unrelated safe work
                       +--> keep irreversible first payment from executing
```

## BANK-ECP bridge

The prize-facing `bank_vendor_onboarding_graph()` binds the `vendor-risk` human decision to the sanitized BANK-ECP gate `BANK_ECP_DORA_VENDOR_RESPONSIBILITY`.

The public bridge is deliberately narrow and development-only. It uses a DORA Article 28(1)(a) responsibility fixture to demonstrate that evidence state changes execution authority. It does not embed the private BANK-ECP runtime and does not claim formal benchmark performance. See [`bank-ecp-bridge.md`](bank-ecp-bridge.md).

A `PASS` verdict does not grant authority. It only makes the evidence side of the human decision eligible once workflow prerequisites are complete. `HOLD` or `ABSTAIN` keeps approval fail-closed. If a previously approved bundle later receives non-PASS evidence, the stale approval is invalidated and the existing correction kernel runs.

## Model-callable boundary

The Strands tool set contains exactly:

- `execute_safe_vendor_work` — executes routine vendor work and the deterministic public evidence check;
- `get_authority_cut` — reads the currently actionable human decisions;
- `execute_authorized_vendor_work` — resumes work using only authority already recorded externally.

There is deliberately no approve, revoke, evidence-correction, or authority-restoration tool. Model wording and model confidence cannot mint a `HumanDecision` or restore stale authority.

## Human authority

The human remains the principal for consequential decisions:

- `vendor-risk` -> `vendor_exception`, `bank_change`;
- `payment-release` -> `payment_enable`;
- `first-funds` -> `funds_release`.

The final irreversible transmit requires `funds_release`. `first-funds` is not ready until the remittance preview has executed; premature approval fails closed.

The historical `vendor_onboarding_graph()` remains as the original controlled 7-protected-effects / 3-semantic-authorities evaluation baseline. The prize-facing `bank_vendor_onboarding_graph()` adds the BANK-ECP evidence gate without rewriting that historical controlled result.

## Evidence-change correction path

The public magic moment is evidence-driven:

1. routine work executes;
2. BANK-ECP bridge evidence is `PASS`;
3. human `vendor-risk` approval is recorded and bound to the evidence digest;
4. protected reversible work executes;
5. the evidence package is corrected and the bridge becomes `HOLD`;
6. `vendor-risk` authority is invalidated as stale;
7. executed reversible descendants receive compensation;
8. unrelated safe actions stay executed;
9. pending irreversible first payment becomes invalidated and cannot execute under stale authority.

Human revocation still uses the same correction kernel and remains available as an independent external principal action.

## Persistence boundary

The competition slice uses process-local control-plane state with synthetic/reference tool effects suitable for public judging. Durable distributed authority state is not claimed. A production deployment would require authenticated principal identity, durable decisions and evidence state, idempotent external tool semantics, compensation verification, concurrency controls, and organization-specific policy validation.

Render-ready Mermaid source: [`architecture.mmd`](architecture.mmd).
