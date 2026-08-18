# Architecture

```text
Professional goal
      |
      v
Strands Agent                         EXTERNAL PRINCIPAL
(central orchestration target)          | approve / deny / revoke
      |                                 |
      | model-callable tools only       v
      |                         Human Authority API
      |                                 |
      +----------------+----------------+
                       v
                Shared ControlPlane
                - action DAG
                - policy bundles
                - exact Authority Cut
                - prerequisite receipts
                - grant store
                - correction propagation
                - compensation ledger
                  |              |
                  |              +--> SQLite reference effects / receipts
                  +--> safe or already-authorized execution
```

## Model-callable boundary

The Strands tool set contains only:

- execute safe vendor work;
- read the current Authority Cut;
- resume work using authority already recorded by the external principal.

There is deliberately no approve/revoke tool. Model wording cannot mint a `HumanDecision` object.

## Workflow authority graph

Seven protected effects are mediated by three semantic decisions:

- `vendor-risk` -> `vendor_exception`, `bank_change`;
- `payment-release` -> `payment_enable`;
- `first-funds` -> `funds_release`.

The final irreversible transmit action requires `funds_release`. `first-funds` is visible as a future decision but is not ready until the remittance-preview action has executed; premature approval fails closed.

## Correction path

Revoking `vendor-risk` finds every descendant that causally depends on the affected protected roots. Executed reversible descendants receive compensation; pending descendants are invalidated; unrelated safe work remains executed. An already-executed irreversible effect can never be labelled rolled back.

## Persistence boundary

The competition slice uses local SQLite-backed reference tool effects plus process-local control-plane state. Durable distributed authority state is not claimed. A production deployment would require authenticated principal identity, durable decisions, idempotent tool semantics, compensation verification and concurrency controls across processes.


Render-ready Mermaid source: [`architecture.mmd`](architecture.mmd).
