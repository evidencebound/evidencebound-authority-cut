# Prior Art and Differentiation

## Fresh official Strands overlap — 2026-08-21

Current Strands Agents documentation already includes a first-class `HumanInTheLoop` intervention handler, interrupt/resume workflows, and `BeforeToolCall` / `BeforeTools` approval interception. Strands can therefore pause an individual tool call or a batch of tool calls and resume after an external human response.

Authority Cut must **not** claim that pausing an agent for approval, allowing safe tools to run, or resuming after human input is novel.

The relevant overlap is especially strong with:

- Strands `HumanInTheLoop`, which can require approval before tool calls and allow-list tools that run without approval;
- Strands interrupt/resume, which preserves execution state while waiting for external human input;
- batch tool approval hooks/interventions;
- agent firewalls and governance-by-construction systems that gate high-risk calls;
- delegation/capability systems that represent revocable authority and least privilege;
- workflow engines and transactional systems with compensation/rollback patterns;
- dynamic approval-routing systems and patent literature that predate this project.

These overlaps eliminate a defensible claim that Authority Cut invented HITL, approval routing, interrupt/resume, revocation, least privilege, dependency invalidation or compensation.

## Candidate competition contribution

Authority Cut operates at a different control granularity from ordinary per-tool approval:

1. protected workflow effects declare required **semantic authority atoms**;
2. policy defines which authority atoms may be granted together as valid semantic decision bundles;
3. the control plane computes the smallest currently actionable policy-valid bundle set rather than asking for every protected tool effect;
4. a decision is not ready until its prerequisite receipts exist;
5. human grant/revocation remains outside the model-callable Strands tool set;
6. a later principal correction is propagated through the action DAG;
7. executed reversible descendants are compensated while unrelated safe work is preserved;
8. a pending irreversible effect is invalidated rather than falsely described as rolled back.

The strongest competition evidence is therefore not “we ask for approval.” It is the observable fixed-workflow path:

`7 protected effects -> 3 semantic authorities -> 6 reversible descendants compensated after correction -> 5 unrelated safe actions preserved -> irreversible transmit invalidated`.

## Falsifiable differentiation thesis

For a multi-step professional workflow with repeated protected effects, a semantic Authority Cut should require fewer human decisions than one approval per protected effect **without** allowing any protected effect outside the policy-authorized semantic authority set. If a later correction revokes an authority that justified already-executed reversible descendants, those descendants should leave the executed state while independent safe ancestors remain executed.

The retained fixed workflow satisfies this mechanism-level test. It does **not** establish a general productivity result or a universal safety guarantee.

## Novelty confidence

**MEDIUM as a competition/product primitive; LOW-MEDIUM as a broad research/patent novelty claim.** Prior-art review is substantial enough to narrow the competition thesis but is not exhaustive legal freedom-to-operate analysis. No “first”, “unique”, “only”, patentability, alignment-solved, or universal self-approval-prevention claim should appear in submission copy.

## Current official references

- Strands Agents — Human in the Loop: https://strandsagents.com/docs/user-guide/concepts/agents/interventions/human-in-the-loop/
- Strands Agents — Interrupts: https://strandsagents.com/docs/user-guide/concepts/interrupts/
- Strands Agents — Tools: https://strandsagents.com/docs/user-guide/concepts/tools/
