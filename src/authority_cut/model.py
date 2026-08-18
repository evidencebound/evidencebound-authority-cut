from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from hashlib import sha256
import json
from typing import Any


def digest(v: Any) -> str:
    return sha256(json.dumps(v,sort_keys=True,separators=(",",":"),default=str).encode()).hexdigest()

class Risk(str,Enum): SAFE="SAFE"; HUMAN="HUMAN"; HIGH="HIGH"
class Status(str,Enum): PENDING="PENDING"; EXECUTED="EXECUTED"; BLOCKED="BLOCKED"; INVALIDATED="INVALIDATED"; ROLLED_BACK="ROLLED_BACK"

@dataclass(frozen=True,slots=True)
class Action:
    action_id:str; tool:str; deps:tuple[str,...]=(); risk:Risk=Risk.SAFE
    authorities:frozenset[str]=field(default_factory=frozenset)
    reversible:bool=True; payload:dict[str,Any]=field(default_factory=dict)

@dataclass(frozen=True,slots=True)
class DecisionBundle:
    bundle_id:str; grants:frozenset[str]; question:str; evidence:tuple[str,...]
    prereqs:tuple[str,...]=()

@dataclass(frozen=True,slots=True)
class HumanDecision:
    bundle_id:str; grants:frozenset[str]; approved:bool; binding:str; rationale:str

@dataclass(slots=True)
class RuntimeState:
    status:dict[str,Status]=field(default_factory=dict)
    decisions:dict[str,HumanDecision]=field(default_factory=dict)
    receipts:list[dict[str,Any]]=field(default_factory=list)
