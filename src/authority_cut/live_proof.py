"""Credential-free live Strands proof for the public judge path.

This module runs the real Strands Agent loop with a deterministic custom Model provider.
It proves SDK orchestration and tool execution without claiming foundation-model or
AgentCore execution. Human authority mutations remain direct external principal calls
on the ControlPlane and are never model-callable tools.
"""
from __future__ import annotations

from typing import Any, AsyncGenerator

from strands.models import Model
from strands.types.content import Messages
from strands.types.streaming import StreamEvent
from strands.types.tools import ToolSpec

from .bank_ecp_bridge import evaluate_bank_ecp_bridge
from .model import Status
from .runtime import get_plane
from .strands_app import STRANDS_TOOL_NAMES, build_agent


class ScriptedToolModel(Model):
    """Deterministic Strands provider that requests a fixed sequence of published tools."""

    def __init__(self, tool_plan: list[str]) -> None:
        self.tool_plan = list(tool_plan)
        self.turn = 0
        self.tool_spec_snapshots: list[list[str]] = []

    def update_config(self, **model_config: Any) -> None:
        return None

    def get_config(self) -> dict[str, Any]:
        return {"provider": "deterministic-public-proof"}

    def structured_output(
        self,
        output_model: Any,
        prompt: Messages,
        system_prompt: str | None = None,
        **kwargs: Any,
    ) -> AsyncGenerator[Any, None]:
        raise NotImplementedError

    async def stream(
        self,
        messages: Messages,
        tool_specs: list[ToolSpec] | None = None,
        system_prompt: str | None = None,
        **kwargs: Any,
    ) -> AsyncGenerator[StreamEvent, None]:
        available = sorted(spec["name"] for spec in (tool_specs or []))
        self.tool_spec_snapshots.append(available)
        yield {"messageStart": {"role": "assistant"}}

        if self.turn < len(self.tool_plan):
            name = self.tool_plan[self.turn]
            if name not in available:
                raise AssertionError(f"planned Strands tool {name!r} not in {available!r}")
            tool_use_id = f"authority-cut-public-{self.turn + 1}"
            self.turn += 1
            yield {
                "contentBlockStart": {
                    "start": {"toolUse": {"name": name, "toolUseId": tool_use_id}}
                }
            }
            yield {"contentBlockDelta": {"delta": {"toolUse": {"input": "{}"}}}}
            yield {"contentBlockStop": {}}
            yield {"messageStop": {"stopReason": "tool_use"}}
            return

        yield {"contentBlockStart": {"start": {}}}
        yield {
            "contentBlockDelta": {
                "delta": {
                    "text": "External human authority is required before further protected work."
                }
            }
        }
        yield {"contentBlockStop": {}}
        yield {"messageStop": {"stopReason": "end_turn"}}


def _invoke_plan(tool_plan: list[str], prompt: str) -> ScriptedToolModel:
    model = ScriptedToolModel(tool_plan)
    agent = build_agent(model=model)
    agent(prompt)
    expected = sorted(STRANDS_TOOL_NAMES)
    if not model.tool_spec_snapshots or any(
        snapshot != expected for snapshot in model.tool_spec_snapshots
    ):
        raise AssertionError(
            f"Strands Agent observed unexpected tool specs: {model.tool_spec_snapshots!r}; "
            f"expected {expected!r}"
        )
    return model


def _public_evidence(decision) -> dict[str, Any]:
    return {
        "case_id": decision.case_id,
        "verdict": decision.verdict.value,
        "reasons": list(decision.reasons),
        "source_locator": decision.source_locator,
        "evidence_class": decision.evidence_class,
    }


def run_live_strands_proof() -> dict[str, Any]:
    """Run the full one-request banking judge sequence through the real Strands Agent loop."""
    p = get_plane(reset=True)
    phases: list[dict[str, Any]] = []

    model = _invoke_plan(
        ["execute_safe_vendor_work", "get_authority_cut"],
        "Begin bank vendor onboarding. Execute routine work, inspect the current human decision, then stop for the human principal.",
    )
    initial_cut = {item["bundle_id"]: item for item in p.decision_surface()}
    supported_evidence = p.state.evidence["vendor-risk"]
    phases.append(
        {
            "phase": "routine-work-and-evidence-check",
            "strands_tool_specs": model.tool_spec_snapshots,
            "bank_ecp_evidence": _public_evidence(supported_evidence),
            "decision_surface": list(initial_cut.values()),
            "status": {k: v.value for k, v in p.state.status.items()},
        }
    )

    if supported_evidence.verdict.value != "PASS":
        raise AssertionError("supported BANK-ECP bridge evidence must pass before vendor-risk review")
    if not initial_cut["vendor-risk"]["ready"]:
        raise AssertionError("vendor-risk must be ready after routine work and evidence PASS")
    if initial_cut["payment-release"]["ready"] or initial_cut["first-funds"]["ready"]:
        raise AssertionError("future authority must not be prematurely ready")

    p.decide("vendor-risk", True, "Public judge external-principal vendor-risk approval")
    model = _invoke_plan(
        ["execute_authorized_vendor_work", "get_authority_cut"],
        "The external human approved vendor-risk. Resume only recorded grants and report the next human decision.",
    )
    phases.append(
        {
            "phase": "human-approved-vendor-risk",
            "strands_tool_specs": model.tool_spec_snapshots,
            "decision_surface": p.decision_surface(),
            "status": {k: v.value for k, v in p.state.status.items()},
        }
    )

    p.decide("payment-release", True, "Public judge external-principal payment-profile approval")
    model = _invoke_plan(
        ["execute_authorized_vendor_work", "get_authority_cut"],
        "The external human approved payment profile setup. Resume authorized work and stop before irreversible first funds.",
    )
    final_cut = {item["bundle_id"]: item for item in p.decision_surface()}
    if set(final_cut) != {"first-funds"} or not final_cut["first-funds"]["ready"]:
        raise AssertionError("first-funds must be the sole ready authority after remittance preview")
    if p.state.status["transmit"] != Status.BLOCKED:
        raise AssertionError("irreversible transmit must remain blocked")
    phases.append(
        {
            "phase": "protected-setup-complete",
            "strands_tool_specs": model.tool_spec_snapshots,
            "decision_surface": list(final_cut.values()),
            "status": {k: v.value for k, v in p.state.status.items()},
        }
    )

    corrected_evidence = evaluate_bank_ecp_bridge("DORA_VENDOR_RESPONSIBILITY_REVERSED")
    affected = p.apply_evidence("vendor-risk", corrected_evidence)
    for action_id in ("activate", "erp_sync", "purchasing", "payments", "terms", "remittance"):
        if p.state.status[action_id] != Status.ROLLED_BACK:
            raise AssertionError(f"{action_id} did not roll back after evidence correction")
    if p.state.status["transmit"] != Status.INVALIDATED:
        raise AssertionError("irreversible transmit must be invalidated after evidence correction")
    for action_id in ("collect", "tax_check", "bank_check", "draft", "followup"):
        if p.state.status[action_id] != Status.EXECUTED:
            raise AssertionError(f"safe action {action_id} was not preserved")

    phases.append(
        {
            "phase": "evidence-changed",
            "trigger": "BANK_ECP_EVIDENCE_CHANGE",
            "bank_ecp_evidence": _public_evidence(corrected_evidence),
            "affected": sorted(affected),
            "status": {k: v.value for k, v in p.state.status.items()},
        }
    )

    return {
        "execution": "REAL_STRANDS_AGENT_LOOP_DETERMINISTIC_MODEL",
        "model_provider": "deterministic-public-proof",
        "strands_tools": list(STRANDS_TOOL_NAMES),
        "authority_mutation_tools": [],
        "authority_boundary": "EXTERNAL_HUMAN_ONLY",
        "correction_trigger": "BANK_ECP_EVIDENCE_CHANGE",
        "bank_ecp_evidence_before_correction": _public_evidence(supported_evidence),
        "bank_ecp_evidence_after_correction": _public_evidence(corrected_evidence),
        "safe_actions_preserved": 5,
        "protected_reversible_effects_rolled_back": 6,
        "irreversible_transmit_after_correction": p.state.status["transmit"].value,
        "foundation_model_invocation": "UNVERIFIED",
        "agentcore": "UNVERIFIED",
        "phases": phases,
        "receipt_count": len(p.state.receipts),
    }
