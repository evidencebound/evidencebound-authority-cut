# BANK-ECP → Authority Cut bridge

Authority Cut uses a deliberately narrow, sanitized BANK-ECP-derived evidence gate in its public bank vendor-onboarding scenario.

## What this bridge does

The public workflow asks a concrete execution question: does the current authoritative evidence support the regulatory premise used for the bank's vendor-risk decision strongly enough for that decision to remain actionable?

The bridge exposes one DORA third-party-risk family with two public development cases:

| Public case | Evidence verdict | Product effect |
| --- | --- | --- |
| `DORA_VENDOR_RESPONSIBILITY_SUPPORTED` | `PASS` | The vendor-risk decision may become ready for a human reviewer once its workflow prerequisites are complete. |
| `DORA_VENDOR_RESPONSIBILITY_REVERSED` | `HOLD` | A previously granted vendor-risk authority becomes stale; affected reversible work is compensated and first payment cannot proceed under that stale authority. |

The authoritative source locator used by both public fixtures is:

**Regulation (EU) 2022/2554, Article 28(1)(a)**.

The supported development proposition is limited to the responsibility point represented by that provision: use of ICT third-party services does not transfer the financial entity's applicable responsibility to the provider. The reversed public case intentionally asserts the opposite and is held with `MATERIAL_CITATION_MISMATCH`.

## Why it is load-bearing

The bridge is not decorative metadata. The prize-facing `bank_vendor_onboarding_graph()` binds the `vendor-risk` human decision to the BANK-ECP gate.

```text
routine vendor work
        ↓
BANK-ECP evidence decision
        ↓
PASS ──────→ vendor-risk may be presented to the human
HOLD/ABSTAIN → vendor-risk cannot be approved
        ↓
external human approval
        ↓
protected vendor setup
        ↓
later evidence PASS → HOLD
        ↓
stale vendor-risk authority invalidated
        ↓
affected reversible work undone
unrelated safe work preserved
first payment blocked from execution
```

Model confidence is not an input that can create or restore authority.

## Evidence classification

This public bridge is deliberately classified:

```text
DEVELOPMENT_ONLY
NOT_FORMAL_BENCHMARK_EVIDENCE
```

**No model-performance result is claimed.**

The bridge does not expose or depend on the private BANK-ECP benchmark runtime, sealed-holdout artifacts, protected benchmark construction internals, or any formal model-comparison result. It does not convert BANK-ECP engineering readiness into empirical superiority.

The public fixture exists to demonstrate the product connection between evidence quality and execution authority.

## Human-authority boundary

Evidence can determine whether an approval remains supportable, but it does not grant human authority itself.

The Strands model-callable tool set remains exactly:

1. `execute_safe_vendor_work`
2. `get_authority_cut`
3. `execute_authorized_vendor_work`

There is no model-callable approve, revoke, evidence-correction, or authority-restoration tool. Human authority mutation remains external to the model tool surface.

## Reproducibility

The bridge implementation is `src/authority_cut/bank_ecp_bridge.py`. Runtime integration is covered by `tests/test_bank_ecp_bridge.py` and `tests/test_banking_product.py`.

The public Strands proof demonstrates the product sequence with a deterministic custom Strands Model provider for credential-free judging. Separate historical native Amazon Bedrock and Amazon Bedrock AgentCore acceptance records remain separately scoped and are not reclassified by this bridge.
