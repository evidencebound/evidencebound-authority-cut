from __future__ import annotations
from itertools import combinations
from .model import Action, DecisionBundle, RuntimeState, Status

class ActionGraph:
    def __init__(self, actions:list[Action], bundles:list[DecisionBundle]):
        self.actions={a.action_id:a for a in actions}; self.bundles={b.bundle_id:b for b in bundles}; self.validate()
    def validate(self):
        for a in self.actions.values():
            for d in a.deps:
                if d not in self.actions: raise ValueError(f"missing dep {d}")
        self.order()
    def order(self):
        incoming={k:set(a.deps) for k,a in self.actions.items()}; out=[]
        ready=sorted(k for k,v in incoming.items() if not v)
        while ready:
            x=ready.pop(0); out.append(x)
            for k in sorted(incoming):
                if x in incoming[k]:
                    incoming[k].remove(x)
                    if not incoming[k] and k not in out and k not in ready: ready.append(k); ready.sort()
        if len(out)!=len(self.actions): raise ValueError("cycle")
        return out
    def descendants(self, roots:set[str])->set[str]:
        out=set(roots); changed=True
        while changed:
            changed=False
            for k,a in self.actions.items():
                if k not in out and set(a.deps)&out: out.add(k); changed=True
        return out
    def unresolved_authorities(self,state:RuntimeState)->set[str]:
        granted=set()
        for d in state.decisions.values():
            if d.approved: granted |= set(d.grants)
        needed=set()
        for aid,a in self.actions.items():
            if state.status.get(aid,Status.PENDING) in {Status.PENDING,Status.BLOCKED}:
                needed |= set(a.authorities)-granted
        return needed
    def minimum_authority_cut(self,state:RuntimeState)->list[DecisionBundle]:
        """Exact minimum policy-defined decision-bundle cover of unresolved authorities.

        Minimality is conditional on the supplied policy-defined bundles. The algorithm
        never invents a broader approval merely to reduce prompts.
        """
        needed=self.unresolved_authorities(state)
        if not needed: return []
        candidates=[b for b in self.bundles.values() if set(b.grants)&needed]
        for size in range(1,len(candidates)+1):
            valid=[]
            for combo in combinations(candidates,size):
                covered=set().union(*(set(b.grants) for b in combo))
                if needed <= covered: valid.append(combo)
            if valid:
                choice=min(valid,key=lambda c:tuple(b.bundle_id for b in c))
                return list(choice)
        raise ValueError(f"no decision bundles cover authorities {sorted(needed)}")
