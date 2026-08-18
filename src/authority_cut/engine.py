from __future__ import annotations
from threading import RLock
from .graph import ActionGraph
from .model import HumanDecision, Risk, RuntimeState, Status, digest
from .tools import VendorTools

class ControlPlane:
    def __init__(self,graph:ActionGraph,tools:VendorTools):
        self.graph=graph; self.tools=tools; self.state=RuntimeState(status={k:Status.PENDING for k in graph.actions}); self._lock=RLock()
    def _deps_done(self,aid): return all(self.state.status[d]==Status.EXECUTED for d in self.graph.actions[aid].deps)
    def _grants(self):
        out=set()
        for d in self.state.decisions.values():
            if d.approved: out |= set(d.grants)
        return out
    def _bundle_ready(self,b):
        return all(self.state.status.get(aid)==Status.EXECUTED for aid in b.prereqs)
    def _prereq_receipts(self,b):
        latest={}
        for receipt in self.state.receipts:
            aid=receipt.get('action')
            if aid in b.prereqs: latest[aid]=receipt.get('result')
        return {aid:latest.get(aid) for aid in b.prereqs}
    def execute_autonomous(self):
        with self._lock:
            progress=True
            while progress:
                progress=False
                for aid in self.graph.order():
                    a=self.graph.actions[aid]
                    if self.state.status[aid]!=Status.PENDING or not self._deps_done(aid): continue
                    if a.risk==Risk.SAFE and not a.authorities:
                        payload={**a.payload,'action_id':aid}; result=self.tools.execute(a.tool,payload)
                        self.state.status[aid]=Status.EXECUTED; self.state.receipts.append({'action':aid,'result':result}); progress=True
                    elif a.authorities:
                        self.state.status[aid]=Status.BLOCKED
            return self.state
    def decision_surface(self):
        with self._lock:
            bundles=self.graph.minimum_authority_cut(self.state)
            return [
                {
                    'bundle_id':b.bundle_id,
                    'question':b.question,
                    'grants':sorted(b.grants),
                    'evidence':list(b.evidence),
                    'prereqs':list(b.prereqs),
                    'ready':self._bundle_ready(b),
                }
                for b in bundles
            ]
    def decide(self,bundle_id:str,approved:bool,rationale:str):
        with self._lock:
            b=self.graph.bundles[bundle_id]
            if approved and not self._bundle_ready(b):
                missing=[aid for aid in b.prereqs if self.state.status.get(aid)!=Status.EXECUTED]
                raise ValueError(f"decision bundle {bundle_id} is not ready; missing executed prerequisites {missing}")
            evidence_binding=self._prereq_receipts(b)
            binding=digest({
                'bundle':b.bundle_id,
                'grants':sorted(b.grants),
                'evidence':b.evidence,
                'prereqs':b.prereqs,
                'prereq_receipts':evidence_binding,
            })
            self.state.decisions[bundle_id]=HumanDecision(bundle_id,b.grants,approved,binding,rationale)
            self.state.receipts.append({
                'human_decision':bundle_id,
                'approved':approved,
                'binding':binding,
                'prereq_receipts':evidence_binding,
            })
            for aid,a in self.graph.actions.items():
                if self.state.status[aid]==Status.BLOCKED and set(a.authorities)<=self._grants(): self.state.status[aid]=Status.PENDING
    def execute_authorized(self):
        with self._lock:
            progress=True
            while progress:
                progress=False
                for aid in self.graph.order():
                    a=self.graph.actions[aid]
                    if self.state.status[aid]!=Status.PENDING or not self._deps_done(aid): continue
                    if set(a.authorities)<=self._grants():
                        payload={**a.payload,'action_id':aid}; result=self.tools.execute(a.tool,payload)
                        self.state.status[aid]=Status.EXECUTED; self.state.receipts.append({'action':aid,'result':result}); progress=True
                    elif a.authorities: self.state.status[aid]=Status.BLOCKED
            return self.state
    def revoke_bundle(self,bundle_id:str,reason:str):
        with self._lock:
            old=self.state.decisions.get(bundle_id)
            if not old: raise KeyError(bundle_id)
            self.state.decisions[bundle_id]=HumanDecision(old.bundle_id,old.grants,False,old.binding,reason)
            roots={aid for aid,a in self.graph.actions.items() if set(a.authorities)&set(old.grants)}
            affected=self.graph.descendants(roots)
            for aid in reversed(self.graph.order()):
                if aid not in affected: continue
                a=self.graph.actions[aid]; status=self.state.status[aid]
                if status==Status.EXECUTED:
                    if a.reversible:
                        self.tools.compensate(a.tool,{**a.payload,'action_id':aid}); self.state.status[aid]=Status.ROLLED_BACK
                    else: self.state.status[aid]=Status.BLOCKED
                elif status in {Status.PENDING,Status.BLOCKED}: self.state.status[aid]=Status.INVALIDATED
            self.state.receipts.append({'correction':bundle_id,'reason':reason,'affected':sorted(affected)})
            return affected
