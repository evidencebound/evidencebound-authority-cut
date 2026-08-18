from __future__ import annotations
from dataclasses import asdict, dataclass
from .engine import ControlPlane
from .model import Status
from .tools import VendorTools
from .workflow import vendor_onboarding_graph


@dataclass(frozen=True, slots=True)
class Evaluation:
    protected_tool_effects: int
    per_tool_hitl_prompts: int
    authority_cut_decisions: int
    prompt_reduction_fraction: float
    safe_actions_before_human: int
    reversible_effects_executed_before_correction: int
    reversible_effects_rolled_back_after_correction: int
    irreversible_effects_executed_without_funds_release: int
    unaffected_safe_actions_preserved: int


def run_evaluation() -> Evaluation:
    p=ControlPlane(vendor_onboarding_graph(),VendorTools.memory())
    protected=sum(1 for a in p.graph.actions.values() if a.authorities)
    p.execute_autonomous()
    safe_before=sum(1 for aid,a in p.graph.actions.items() if not a.authorities and p.state.status[aid]==Status.EXECUTED)
    cut=len(p.decision_surface())
    p.decide('vendor-risk',True,'evaluation approval'); p.execute_authorized()
    p.decide('payment-release',True,'evaluation approval'); p.execute_authorized()
    reversible_before=sum(1 for aid,a in p.graph.actions.items() if a.authorities and a.reversible and p.state.status[aid]==Status.EXECUTED)
    irreversible_without=sum(1 for aid,a in p.graph.actions.items() if a.authorities and not a.reversible and p.state.status[aid]==Status.EXECUTED)
    p.revoke_bundle('vendor-risk','evaluation correction')
    rolled=sum(1 for aid,a in p.graph.actions.items() if a.authorities and a.reversible and p.state.status[aid]==Status.ROLLED_BACK)
    unaffected=sum(1 for aid,a in p.graph.actions.items() if not a.authorities and p.state.status[aid]==Status.EXECUTED)
    return Evaluation(
        protected_tool_effects=protected,
        per_tool_hitl_prompts=protected,
        authority_cut_decisions=cut,
        prompt_reduction_fraction=(protected-cut)/protected,
        safe_actions_before_human=safe_before,
        reversible_effects_executed_before_correction=reversible_before,
        reversible_effects_rolled_back_after_correction=rolled,
        irreversible_effects_executed_without_funds_release=irreversible_without,
        unaffected_safe_actions_preserved=unaffected,
    )
