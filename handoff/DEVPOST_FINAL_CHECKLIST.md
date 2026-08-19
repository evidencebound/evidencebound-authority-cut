# Authority Cut — Devpost Final Checklist

Snapshot: 2026-08-19

## Competition

**AWS Agents for Humans**

- submission deadline: **2026-09-14 17:00 PT / 2026-09-15 00:00 UTC**;
- target prize track: **Professional Agents**;
- public video: YouTube or Vimeo, maximum **5 minutes**;
- AWS Builder ID required by the submission flow;
- public source repository required;
- README + architecture documentation required;
- MIT or Apache license required — Authority Cut uses **Apache-2.0**;
- pre-existing work must be disclosed.

## Canonical submission links

**Public repository**

`https://github.com/moneyparking/evidencebound-authority-cut`

**Public functional judge URL**

`https://evidencebound-authority-cut.vercel.app`

## Engineering readiness

- Strands architecturally central: **PASS**
- real Strands SDK Agent loop: **PASS**
- real tool execution: **PASS**
- one deep professional workflow: **PASS**
- selective external human intervention: **PASS**
- human correction changes downstream execution: **PASS**
- reversible recovery/compensation: **PASS**
- irreversible-effect gating: **PASS**
- provenance/receipts: **PASS**
- public repo: **PASS**
- public CI: **PASS**
- public judge URL: **PASS**
- Apache-2.0 license: **PASS**
- pre-existing-work disclosure: **PASS**
- foundation-model execution: **UNRUN / optional score upgrade**
- AgentCore deployment: **UNRUN / optional score upgrade**

## Judge test path

1. Open `https://evidencebound-authority-cut.vercel.app`.
2. Verify the page states the truth boundary: real Strands loop; deterministic custom Model; foundation model and AgentCore unverified.
3. Select **Run live Strands judge path**.
4. Confirm five safe actions execute and `vendor-risk` is the only ready authority initially.
5. Confirm model-callable tools contain no approve/revoke function.
6. Inspect the next phase after the external `vendor-risk` grant.
7. Inspect `payment-release` and then `first-funds` readiness.
8. Confirm irreversible `transmit` remains blocked before first-funds authority.
9. Inspect the correction phase: six protected reversible effects `ROLLED_BACK`, transmit `INVALIDATED`, five safe actions preserved.
10. Cross-check `/api/tool-boundary` and `/api/evaluation` if desired.

## Stage Two judging mapping

### Technical Implementation

Lead with live Strands execution + external human authority boundary + correction propagation. Do not lead with optional AgentCore.

### Design

Show the decision surface: routine work is autonomous; only currently actionable semantic authority is escalated; future decisions stay hidden/not-ready.

### Potential Impact

Describe professional operations use cases. Keep the 57.14% reduction explicitly scoped to the fixed vendor-onboarding workflow. Do not claim measured customer productivity.

### Creativity & Originality

Use the invention thesis **Authority Cut Sets + Reversible Correction Propagation** and disclose overlap with HITL, provenance, dependency invalidation and compensation patterns.

### Presentation

Spend video time on the four-phase live proof, not infrastructure setup.

## Video capture checklist

- [ ] Problem statement: too many interruptions vs silent authority accumulation.
- [ ] Show public URL and repo identity.
- [ ] Show exact Strands tool list; highlight no approve/revoke tool.
- [ ] Run live proof: safe work.
- [ ] Show initial Authority Cut readiness.
- [ ] Show external vendor-risk grant and authorized resume.
- [ ] Show payment-release grant and remittance preview.
- [ ] Show first-funds ready while transmit remains blocked.
- [ ] Revoke vendor-risk.
- [ ] Show six rollbacks, transmit invalidated, five safe actions preserved.
- [ ] Show evidence/receipts/public CI briefly.
- [ ] State limitations: deterministic live model provider, no AgentCore claim, fixed-workflow metrics only.
- [ ] Keep final published video <=5 minutes and public on YouTube/Vimeo.

## Form / identity actions

- [ ] Confirm hackathon registration / official rules acceptance if not already completed.
- [ ] Confirm AWS Builder ID for the entrant.
- [ ] Add project name `Authority Cut`.
- [ ] Add public repository URL.
- [ ] Add public functional judge URL.
- [ ] Add public video URL.
- [ ] Add architecture diagram / architecture description as requested by the form.
- [ ] Include pre-existing-work disclosure from `docs/preexisting-work.md`.
- [ ] Ensure all written claims match `AWS_JUDGE_PACK.md`, `docs/claims-ledger.md`, and `qa/QA_RECEIPT.json`.
- [ ] Final Devpost submission remains an owner action.

## Optional score upgrades — not required for READY

### AWS promotional credits

Registered participants may request the current competition AWS promotional credit while supplies remain available. Current organizer deadline: **2026-09-11 12:00 PT**.

Use only if pursuing verified AWS/AgentCore work; do not request credits merely for a logo/checkbox.

### AgentCore

Current blocker: `BLOCKED_AWS_OIDC_TRUST`.

Owner action: create/extend a least-privilege GitHub OIDC trust for `moneyparking/evidencebound-authority-cut`, then verify STS identity before any resource mutation.

### Foundation-model acceptance

Current blocker: `BLOCKED_RUNTIME_GATEWAY_CREDENTIAL`.

Provider adapter and fail-closed contract are already PASS. Actual invocation stays UNRUN until a supported runtime credential exists.

### builder.aws bonus content

If pursuing the current content bonus, produce only technically substantive posts that document the actual mechanism/evidence. Do not let bonus-content work displace the final video/submission or destabilize the live demo.

## Final status

**READY** — required engineering and live judge path are complete. Remaining required work is registration/identity verification if needed, final media, Devpost form completion and submission.
