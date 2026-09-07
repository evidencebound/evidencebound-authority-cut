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

from .bank_ecp_bridge import evaluate_bank_ecp_bridge
from .runtime import get_plane


@tool
def execute_safe_vendor_work()->dict[str,Any]:
    """Execute routine vendor work and its deterministic BANK-ECP evidence check."""
    p=get_plane(); p.execute_autonomous()
    if 'vendor-risk' not in p.state.evidence:
        p.apply_evidence(
            'vendor-risk',
            evaluate_bank_ecp_bridge('DORA_VENDOR_RESPONSIBILITY_SUPPORTED'),
        )
    return {
        'status':{k:v.value for k,v in p.state.status.items()},
        'evidence':{
            k:{'case_id':v.case_id,'verdict':v.verdict.value,'reasons':list(v.reasons),'source_locator':v.source_locator,'evidence_class':v.evidence_class}
            for k,v in p.state.evidence.items()
        },
        'receipts':p.state.receipts,
    }


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

SYSTEM_PROMPT=(
    "You are a bank vendor-onboarding operations agent. Execute routine work through "
    "execute_safe_vendor_work, which also runs the deterministic regulatory evidence "
    "check, then inspect get_authority_cut and surface only ready human decisions. "
    "Human approvals/revocations arrive outside your tool set. After the external "
    "principal acts, call execute_authorized_vendor_work. Never treat model confidence "
    "as authority and never claim that you approved, revoked, or bypassed a decision."
)


def build_agent(*, model: Any | None = None):
    """Construct the Strands Agent while retaining external principal authority.

    `model` injection exists for deterministic SDK/tool-loop acceptance tests and for
    explicit production provider selection. Omitting it preserves Strands' configured
    default model provider behavior.
    """
    if Agent is None:
        raise RuntimeError('strands-agents is not installed')
    kwargs: dict[str, Any] = {
        'system_prompt': SYSTEM_PROMPT,
        'tools': STRANDS_TOOLS,
    }
    if model is not None:
        kwargs['model'] = model
    return Agent(**kwargs)
