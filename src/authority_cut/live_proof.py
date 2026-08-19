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


def run_live_strands_proof() -> dict[str, Any]:
    """Run the full one-request judge sequence through the real Strands Agent loop."""
    p = get_plane(reset=True)
    phases: list[dict[str, Any]] = []

    model = _invoke_plan(
        ["execute_safe_vendor_work", "get_authority_cut"],
        "Begin vendor onboarding. Execute safe work, inspect the authority cut, then stop for the human principal.",
    )
    initial_cut = {item["bundle_id"]: item for item in p.decision_surface()}
    phases.append(
        {
            "phase": "safe-work-and-cut",
            "strands_tool_specs": model.tool_spec_snapshots,
            "decision_surface": list(initial_cut.values()),
            "status": {k: v.value for k, v in p.state.status.items()},
        }
    )

    if not initial_cut["vendor-risk"]["ready"]:
        raise AssertionError("vendor-risk must be ready after safe work")
    if initial_cut["payment-release"]["ready"] or initial_cut["first-funds"]["ready"]:
        raise AssertionError("future authority must not be prematurely ready")

    p.decide("vendor-risk", True, "Public judge external-principal approval")
    model = _invoke_plan(
        ["execute_authorized_vendor_work", "get_authority_cut"],
        "The external principal approved vendor-risk. Resume only recorded grants and report the next authority cut.",
    )
    phases.append(
        {
            "phase": "vendor-risk-authorized",
            "strands_tool_specs": model.tool_spec_snapshots,
            "decision_surface": p.decision_surface(),
            "status": {k: v.value for k, v in p.state.status.items()},
        }
    )

    p.decide("payment-release", True, "Public judge external-principal approval")
    model = _invoke_plan(
        ["execute_authorized_vendor_work", "get_authority_cut"],
        "The external principal approved payment-release. Resume authorized work and stop before irreversible funds release.",
    )
    final_cut = {item["bundle_id"]: item for item in p.decision_surface()}
    if set(final_cut) != {"first-funds"} or not final_cut["first-funds"]["ready"]:
        raise AssertionError("first-funds must be the sole ready authority after remittance preview")
    if p.state.status["transmit"] != Status.BLOCKED:
        raise AssertionError("irreversible transmit must remain blocked")
    phases.append(
        {
            "phase": "payment-release-authorized",
            "strands_tool_specs": model.tool_spec_snapshots,
            "decision_surface": list(final_cut.values()),
            "status": {k: v.value for k, v in p.state.status.items()},
        }
    )

    affected = p.revoke_bundle("vendor-risk", "Public judge external-principal correction")
    for action_id in ("activate", "erp_sync", "purchasing", "payments", "terms", "remittance"):
        if p.state.status[action_id] != Status.ROLLED_BACK:
            raise AssertionError(f"{action_id} did not roll back")
    if p.state.status["transmit"] != Status.INVALIDATED:
        raise AssertionError("irreversible transmit must be invalidated after correction")
    for action_id in ("collect", "tax_check", "bank_check", "draft", "followup"):
        if p.state.status[action_id] != Status.EXECUTED:
            raise AssertionError(f"safe action {action_id} was not preserved")

    phases.append(
        {
            "phase": "human-correction",
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
        "safe_actions_preserved": 5,
        "protected_reversible_effects_rolled_back": 6,
        "irreversible_transmit_after_correction": p.state.status["transmit"].value,
        "foundation_model_invocation": "UNVERIFIED",
        "agentcore": "UNVERIFIED",
        "phases": phases,
        "receipt_count": len(p.state.receipts),
    }
