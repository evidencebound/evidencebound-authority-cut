"""Single-process competition runtime state.

The human API and the Strands orchestration adapter intentionally share this store so
external authority decisions govern the exact state that the agent can execute.
A production AgentCore deployment should replace this process-local singleton with a
durable store; authority semantics must remain outside model control.
"""
from __future__ import annotations
from threading import RLock

from .engine import ControlPlane
from .tools import VendorTools
from .workflow import vendor_onboarding_graph

_LOCK=RLock()
_PLANE: ControlPlane | None=None


def get_plane(*, reset: bool=False) -> ControlPlane:
    global _PLANE
    with _LOCK:
        if reset or _PLANE is None:
            _PLANE=ControlPlane(vendor_onboarding_graph(),VendorTools.memory())
        return _PLANE
