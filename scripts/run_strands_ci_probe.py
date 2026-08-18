"""Networked CI proof that the real Strands Agent loop executes Authority Cut tools.

This deliberately uses a deterministic custom Strands Model provider so the public CI
probe requires no external model credentials. It proves SDK Agent-loop/tool execution,
not foundation-model quality or Bedrock/AgentCore deployment.
"""
from __future__ import annotations

import json
from typing import Any, AsyncGenerator

from strands.models import Model
from strands.types.content import Messages
from strands.types.streaming import StreamEvent
from strands.types.tools import ToolSpec

from authority_cut.model import Status
from authority_cut.runtime import get_plane
from authority_cut.strands_app import STRANDS_TOOL_NAMES, build_agent


class ScriptedToolModel(Model):
    """Minimal deterministic provider that asks Strands to execute named tools in order."""

    def __init__(self, tool_plan: list[str]) -> None:
        self.tool_plan = list(tool_plan)
        self.turn = 0
        self.tool_spec_snapshots: list[list[str]] = []

    def update_config(self, **model_config: Any) -> None:
        return None

    def get_config(self) -> dict[str, Any]:
        return {"provider": "deterministic-ci-proof"}

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
            tool_use_id = f"authority-cut-ci-{self.turn + 1}"
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
                "delta": {"text": "External human authority is required before further protected work."}
            }
        }
        yield {"contentBlockStop": {}}
        yield {"messageStop": {"stopReason": "end_turn"}}


def invoke_plan(tool_plan: list[str], prompt: str) -> ScriptedToolModel:
    model = ScriptedToolModel(tool_plan)
    agent = build_agent(model=model)
    agent(prompt)
    expected = sorted(STRANDS_TOOL_NAMES)
    if not model.tool_spec_snapshots or any(snapshot != expected for snapshot in model.tool_spec_snapshots):
        raise AssertionError(
            f"Strands Agent observed unexpected tool specs: {model.tool_spec_snapshots!r}; expected {expected!r}"
        )
    return model


def main() -> int:
    p = get_plane(reset=True)

    invoke_plan(
        ["execute_safe_vendor_work", "get_authority_cut"],
        "Begin vendor onboarding. Execute safe work, inspect the authority cut, then stop for the human principal.",
    )
    assert p.state.status["draft"] == Status.EXECUTED
    assert p.state.status["followup"] == Status.EXECUTED
    assert p.state.status["activate"] == Status.BLOCKED
    initial_cut = {item["bundle_id"]: item for item in p.decision_surface()}
    assert initial_cut["vendor-risk"]["ready"] is True
    assert initial_cut["payment-release"]["ready"] is False
    assert initial_cut["first-funds"]["ready"] is False

    # Authority is intentionally injected outside the Strands model-callable tool set.
    p.decide("vendor-risk", True, "CI external-principal approval")
    invoke_plan(
        ["execute_authorized_vendor_work", "get_authority_cut"],
        "The external principal acted. Resume only work authorized by the recorded grants and report the next cut.",
    )
    assert p.state.status["activate"] == Status.EXECUTED
    assert p.state.status["payments"] == Status.BLOCKED

    p.decide("payment-release", True, "CI external-principal approval")
    invoke_plan(
        ["execute_authorized_vendor_work", "get_authority_cut"],
        "The external principal acted again. Resume only authorized work and stop before irreversible funds release.",
    )
    assert p.state.status["remittance"] == Status.EXECUTED
    assert p.state.status["transmit"] == Status.BLOCKED
    final_cut = {item["bundle_id"]: item for item in p.decision_surface()}
    assert set(final_cut) == {"first-funds"}
    assert final_cut["first-funds"]["ready"] is True

    affected = p.revoke_bundle("vendor-risk", "CI external-principal correction")
    expected_affected = {
        "activate",
        "erp_sync",
        "purchasing",
        "payments",
        "terms",
        "remittance",
        "transmit",
    }
    assert affected == expected_affected
    for action_id in ("activate", "erp_sync", "purchasing", "payments", "terms", "remittance"):
        assert p.state.status[action_id] == Status.ROLLED_BACK
    assert p.state.status["transmit"] == Status.INVALIDATED
    for action_id in ("collect", "tax_check", "bank_check", "draft", "followup"):
        assert p.state.status[action_id] == Status.EXECUTED

    print(
        json.dumps(
            {
                "execution": "REAL_STRANDS_AGENT_LOOP_DETERMINISTIC_MODEL",
                "strands_tools": list(STRANDS_TOOL_NAMES),
                "authority_mutation_tools": [],
                "safe_actions_preserved": 5,
                "protected_reversible_effects_rolled_back": 6,
                "irreversible_transmit_after_correction": p.state.status["transmit"].value,
                "foundation_model_invocation": "UNVERIFIED",
                "agentcore": "UNVERIFIED",
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
