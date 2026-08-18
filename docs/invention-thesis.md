# Invention Thesis — Authority Cut Sets + Reversible Correction Propagation

## Problem

Per-tool HITL can turn a professional agent into an approval queue. Broad one-shot approval reduces interruption but expands consent scope. The missing product primitive is a way to expose a small human decision surface without letting the model manufacture broader authority, then preserve human control when an already-issued decision is later corrected.

## Mechanism

Each protected action declares semantic authority atoms. Policy defines the only valid `DecisionBundle`s that a principal may approve. The runtime computes an exact minimum set cover of unresolved authority atoms **using only those policy-defined bundles**. It never synthesizes a broader approval merely to reduce prompts.

A bundle may also require executed prerequisites. Approval is cryptographically bound to the bundle, grants and prerequisite receipts. Protected effects remain outside model authority. After an external principal revokes a bundle, the runtime propagates that correction through authority-dependent descendants and compensates executed reversible effects.

## Fixed-workflow result

The current vendor-onboarding graph has 7 protected effects and 3 semantic authority bundles. In the controlled path, 5 safe actions run before human attention, six reversible protected effects execute after the first two decisions, first-funds remains separately blocked, and revoking vendor-risk rolls back all six reversible descendants while preserving the five safe actions.

## Falsifiable properties

1. With complete mediation, no protected action executes without all required current grants.
2. The returned decision surface is minimal relative to the policy-defined bundle set.
3. A bundle cannot be approved before its declared prerequisites execute.
4. Revoking authority after partial execution compensates reversible affected descendants and preserves independent completed work.
5. The model cannot issue/revoke human authority through its published Strands tool set.

## Novelty boundary

HITL, tool approval, delegated authorization, least privilege, policy firewalls, dynamic approval routes and rollback are established prior art. The competition thesis is the concrete combination of **plan-level semantic Authority Cut computation**, externally held principal authority, prerequisite-bound decisions and correction-driven selective compensation. No “first” or patent-novel claim is made.
