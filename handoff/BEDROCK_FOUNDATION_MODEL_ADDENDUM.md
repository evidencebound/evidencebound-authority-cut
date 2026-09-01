# Authority Cut — Native Amazon Bedrock Foundation-Model Addendum

Snapshot: 2026-09-01

## Decision

**FOUNDATION-MODEL EXECUTION: PASS**

This addendum updates the AWS judge/submission handoff with a later, independently executed native Amazon Bedrock acceptance. It must be read together with `AWS_JUDGE_PACK.md` and `docs/bedrock-foundation-model-acceptance-2026-09-01.md`.

## Judge-ready claim

A real Amazon Nova Lite foundation model, invoked through native Amazon Bedrock by a Strands Agent in `eu-central-1`, executed the Authority Cut workflow while the model-callable surface remained exactly the three non-authorizing tools and human authority mutation remained external to the model.

Exact accepted source:

`9998565c6db8083446caef7e20a6cf03601533e6`

AWS target:

- region: `eu-central-1`;
- inference profile: `eu.amazon.nova-lite-v1:0`;
- profile status: `ACTIVE`;
- profile type: `SYSTEM_DEFINED`;
- target model count: 4.

Independent direct Bedrock Runtime probe:

```text
DIRECT_CONVERSE=PASS
STOP_REASON=end_turn
INPUT_TOKENS=8
OUTPUT_TOKENS=5
TOTAL_TOKENS=13
```

Full Authority Cut Strands acceptance:

```text
AUTHORITY_CUT_BEDROCK=PASS
EXECUTION=REAL_STRANDS_AGENT_LOOP_FOUNDATION_MODEL
FOUNDATION_MODEL_INVOCATION=PASS
```

## Authority boundary preserved

Model-callable tools remained exactly:

1. `execute_safe_vendor_work`
2. `get_authority_cut`
3. `execute_authorized_vendor_work`

`authority_mutation_tools=[]` remains the design invariant. Approve and revoke remain external-principal actions.

The live model sequence stopped at each unresolved authority and did not invent approval. It progressed only after external grants for `vendor-risk` and `payment-release`, then stopped before `first-funds` and irreversible transmit.

The fail-closed acceptance code promotes PASS only after verifying positive model usage, three distinct response receipts, preservation of 5 safe actions, rollback of all 6 executed reversible protected effects after correction, and invalidation of pending irreversible transmit.

## What to say to judges

Use this sentence:

> Authority Cut now has two complementary proofs: a credential-free deterministic public Strands judge path for reproducibility, and a separately verified native Amazon Bedrock / Amazon Nova Lite Strands acceptance showing that the same human-control boundary survives a real foundation-model execution.

## What not to say

Do not say:

- the public Vercel judge route is Bedrock-backed;
- the 2026-08-23 AgentCore Runtime invocation was foundation-model-backed;
- the older Vercel AI Gateway attempt invoked a model;
- foundation-model PASS proves general safety, alignment or corrigibility.

## Submission text patch

If the Devpost technical description can still be edited without jeopardizing submission state, add a concise verified note such as:

> Additional production-depth acceptance: the same three-tool Strands Authority Cut workflow was executed with Amazon Nova Lite through native Amazon Bedrock in eu-central-1. Direct Bedrock Runtime Converse passed, and the full Strands workflow returned `REAL_STRANDS_AGENT_LOOP_FOUNDATION_MODEL` with `FOUNDATION_MODEL_INVOCATION=PASS` while approve/revoke remained outside the model tool surface. The public judge URL intentionally remains deterministic and credential-free.

Do not replace the existing video or imply the video shows this later acceptance.

## Competition value

This closes the main prior evidence gap: earlier evidence proved real Strands execution and real AgentCore infrastructure but not a foundation-model-backed Strands run. The native Bedrock acceptance now provides that missing proof without weakening the human authority boundary or making the public judge path dependent on paid credentials.
