"""Competition-period Strands orchestration adapter.

Strands is the professional workflow orchestrator, but it is deliberately *not* an
authority issuer. Human approvals and revocations enter through the external human
control API and are therefore absent from the model-callable tool set.
"""
from __future__ import annotations
from typing import Any

try:
    from strands import Agent, tool
except ImportError:  # deterministic kernel remains locally testable without SDK
    Agent = None
    def tool(fn): return fn

from .runtime import get_plane


@tool
def execute_safe_vendor_work()->dict[str,Any]:
    """Execute currently eligible safe vendor-onboarding work."""
    p=get_plane(); p.execute_autonomous()
    return {'status':{k:v.value for k,v in p.state.status.items()},'receipts':p.state.receipts}


@tool
def get_authority_cut()->dict[str,Any]:
    """Read policy-defined human decisions; never approve them."""
    return {'decisions':get_plane().decision_surface()}


@tool
def execute_authorized_vendor_work()->dict[str,Any]:
    """Resume work using only grants already recorded by the external human API."""
    p=get_plane(); p.execute_authorized()
    return {'status':{k:v.value for k,v in p.state.status.items()},'decision_surface':p.decision_surface()}


STRANDS_TOOLS=[execute_safe_vendor_work,get_authority_cut,execute_authorized_vendor_work]
STRANDS_TOOL_NAMES=('execute_safe_vendor_work','get_authority_cut','execute_authorized_vendor_work')


def build_agent():
    if Agent is None:
        raise RuntimeError('strands-agents is not installed')
    return Agent(
        system_prompt=(
            "You are a vendor-onboarding operations agent. Execute routine work through "
            "execute_safe_vendor_work, inspect get_authority_cut, and surface its ready human "
            "decisions without changing them. Human approvals/revocations arrive outside your "
            "tool set. After the external principal acts, call execute_authorized_vendor_work. "
            "Never claim that you approved, revoked, or bypassed an authority decision."
        ),
        tools=STRANDS_TOOLS,
    )
