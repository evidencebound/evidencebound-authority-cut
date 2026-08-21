# builder.aws Bonus Post Pack — Authority Cut

Prepared for the **Agents for Humans Hackathon**. Current Official Rules allow up to three public builder.aws posts for up to **0.6 bonus points total (0.2 each)**. The rules were updated 2026-08-12 to remove the old hashtag requirement; keep **“Agents for Humans”** in each title.

All claims below are scoped to the verified fixed vendor-onboarding workflow. Do not add AgentCore or foundation-model execution claims unless those paths are independently accepted later.

---

# Post 1 — Agents for Humans: Compressing Human Authority with Authority Cut Sets

Professional agents face a control problem that ordinary tool calling does not solve by itself. If every protected tool call asks for approval, the agent may be safe in a narrow sense but becomes an interrupt generator. If the system instead gives broad standing permission so the agent can keep moving, human authority can become wider than the operator intended.

For the Agents for Humans Hackathon I built **Authority Cut**, a Strands Agents professional-agent prototype for vendor onboarding. The core idea is to separate **execution tools** from **authority** and to compress the human decision surface at the semantic level rather than at the individual tool-call level.

The published Strands agent has exactly three model-callable tools:

1. `execute_safe_vendor_work`
2. `get_authority_cut`
3. `execute_authorized_vendor_work`

Approve and revoke are not Strands tools exposed to the model. They are external principal actions recorded in a shared control plane.

This distinction matters because Strands already provides strong human-in-the-loop primitives. Its `HumanInTheLoop` intervention and interrupt/resume system can pause before individual or batched tool calls. Authority Cut is not an attempt to reinvent that. Instead, it asks a different question: **what is the smallest policy-valid semantic authority the human must decide now for the workflow to make useful progress?**

The fixed vendor workflow contains five safe routine actions and seven protected downstream effects. Those seven protected effects are governed by three semantic authority bundles:

- `vendor-risk`
- `payment-release`
- `first-funds`

A bundle becomes actionable only after its prerequisites and evidence receipts exist. At the start, `vendor-risk` is ready while `payment-release` and `first-funds` remain future decisions. After the external principal grants `vendor-risk`, the Strands agent resumes activation, ERP synchronization, and purchasing. Only then does `payment-release` become ready. After that decision, the agent can prepare the payment profile, terms, and remittance preview. The preview receipt is what makes `first-funds` ready.

The irreversible transfer remains separately gated. The public proof never executes it.

In this fixed workflow, a one-approval-per-protected-effect baseline would request seven decisions. Authority Cut requests three semantic decisions, a **57.14% reduction in this controlled workflow**. That number is not a customer productivity claim; it is simply a mechanism-level comparison for the published graph.

The more important property is that no protected effect becomes executable just because the agent wants to continue. The current authority set, policy bundles, dependency graph, and receipts determine what is possible.

The public judge path runs a real Strands SDK Agent/tool loop with a deterministic custom model provider and exposes the exact tool boundary and current decision surface:

https://evidencebound-authority-cut.vercel.app

Source:

https://github.com/moneyparking/evidencebound-authority-cut

The design goal is not “remove the human.” It is **remove unnecessary human interruptions while preserving the human’s authority over the decisions that actually matter**.

---

# Post 2 — Agents for Humans: Making Human Corrections Change What an Agent Already Did

Human-in-the-loop approval usually focuses on the moment before an action executes. That is important, but long-running professional workflows have another problem: **what happens when the human changes their mind after downstream work has already happened?**

Authority Cut treats correction as an executable control-plane event rather than an audit annotation.

The competition workflow is vendor onboarding. A Strands agent completes five safe tasks autonomously, then waits for semantic authority before protected effects. An external human principal grants `vendor-risk`, allowing activation, ERP synchronization, and purchasing. Later the principal grants `payment-release`, allowing the payment profile, terms, and remittance preview to execute. The final irreversible transmission still requires a separate `first-funds` authority and remains blocked.

Now introduce the adversarial case: the human revokes the earlier `vendor-risk` decision after six reversible protected effects have already executed.

A weak implementation might simply append “approval revoked” to a log while leaving the downstream state untouched. Another weak implementation might erase the entire workflow and destroy unrelated useful work.

Authority Cut instead propagates the correction through the action dependency graph.

In the retained fixed workflow:

- six already-executed reversible protected descendants become `ROLLED_BACK` through compensation;
- the pending irreversible transmission becomes `INVALIDATED`;
- five unrelated safe actions remain `EXECUTED`.

This is deliberately not described as universal rollback. Some effects cannot be reversed. That is why the irreversible `transmit` action is modeled separately and never falsely reported as rolled back. If upstream authority disappears before transmission, the pending irreversible effect becomes invalid for the current workflow state.

The same discipline applies to the human/model boundary. The Strands tool schema lets the model execute safe work, inspect the Authority Cut, and execute work that is already authorized. It does not expose approve or revoke as model-callable tools. The external principal channel changes the authority state the agent observes when it resumes.

The live public proof returns the four phases and their action states from a real Strands SDK tool loop. The final correction phase is machine-readable, including the six rollbacks, the invalidated transfer, and the five safe actions preserved.

Live proof:

https://evidencebound-authority-cut.vercel.app/api/strands-proof-get

Repository:

https://github.com/moneyparking/evidencebound-authority-cut

This mechanism builds on existing ideas rather than claiming to invent them. Workflow systems already have compensation transactions. Agent systems already have human approval and interrupt/resume. Dependency invalidation and revocable authority also have substantial prior art.

The competition contribution is the concrete composition: **semantic authority bundles determine which protected effects may execute, and a later human correction changes the state of already-executed reversible descendants without deleting unrelated safe work.**

For professional agents, correction needs to be operational. A human changing the decision should change the system, not just the story the audit log tells about it.

---

# Post 3 — Agents for Humans: Keeping Irreversible Actions Outside the Agent’s Authority

Autonomous professional workflows become most dangerous at their irreversible boundary. Drafting a record, preparing a payment profile, or generating a remittance preview can often be compensated or replaced. Actually transmitting funds is different.

Authority Cut models that difference explicitly.

The prototype is built with Strands Agents for a vendor-onboarding workflow. The agent can autonomously complete safe routine work and, after external human authority is recorded, execute protected reversible work. But the first actual funds transmission is not bundled into the same decision as routine payment setup.

It has its own semantic authority: `first-funds`.

That authority is not even ready at the beginning of the workflow. It requires a remittance-preview receipt. The sequence is:

1. the agent completes safe vendor checks and preparation;
2. an external human grants `vendor-risk`;
3. the agent executes the reversible vendor-activation branch;
4. an external human grants `payment-release`;
5. the agent builds payment configuration and a remittance preview;
6. the preview receipt makes `first-funds` ready;
7. actual transmission remains `BLOCKED` until that distinct authority exists.

The public demonstration deliberately stops before transmitting anything. It uses synthetic in-memory workflow state and creates no external vendor or payment effects.

This architecture matters for two reasons.

First, it prevents a broad earlier decision from silently authorizing a later irreversible effect. “Approve this vendor” is not equivalent to “release funds.” The authority model preserves that semantic distinction.

Second, correction remains meaningful. In the demonstration, the human later revokes `vendor-risk`. Six reversible protected effects are compensated. Because the upstream authority chain has changed, the pending transmission becomes `INVALIDATED`. It is not called “rolled back” because it was never executed.

The Strands capability boundary is equally explicit. The model-callable tools are execution and inspection tools. The model does not receive an approve/revoke tool in the published interface. Human authority arrives through an external principal channel and is evaluated by the control plane before protected work can resume.

Authority Cut is not a claim that every irreversible action in every domain can be modeled perfectly, or that the system solves agent safety. It is a production-oriented control primitive with falsifiable behavior in one deep professional workflow.

The current live path is intentionally honest about its infrastructure boundary. It executes a real Strands SDK Agent/tool loop with a deterministic custom model provider. Foundation-model invocation and Amazon Bedrock AgentCore deployment remain unverified and are not claimed as completed.

Live judge path:

https://evidencebound-authority-cut.vercel.app

Public code and test instructions:

https://github.com/moneyparking/evidencebound-authority-cut

For autonomous agents that touch professional operations, a useful rule is simple: **reversible preparation can be automated aggressively; irreversible commitment deserves its own explicit authority boundary.**
