import importlib.util
import pytest
from authority_cut.demo import run_demo
from authority_cut.engine import ControlPlane
from authority_cut.model import Status
from authority_cut.tools import VendorTools
from authority_cut.workflow import vendor_onboarding_graph

def make(): return ControlPlane(vendor_onboarding_graph(),VendorTools.memory())

def test_safe_work_runs_without_human_interrupt():
 p=make(); p.execute_autonomous();
 assert p.state.status['draft']==Status.EXECUTED
 assert p.state.status['followup']==Status.EXECUTED
 assert p.state.status['activate']==Status.BLOCKED

def test_authority_cut_is_two_policy_defined_decisions_not_per_action_prompts():
 p=make(); p.execute_autonomous(); s=p.decision_surface()
 assert {x['bundle_id'] for x in s}=={'vendor-risk','payment-release','first-funds'}
 assert len(s)==3

def test_first_decision_unlocks_activation_but_not_payments():
 p=make(); p.execute_autonomous(); p.decide('vendor-risk',True,'ok'); p.execute_authorized()
 assert p.state.status['activate']==Status.EXECUTED
 assert p.state.status['payments']==Status.BLOCKED
 assert {x['bundle_id'] for x in p.decision_surface()}=={'payment-release','first-funds'}

def test_correction_rolls_back_descendants_and_preserves_unaffected_work():
 p=make(); p.execute_autonomous(); p.decide('vendor-risk',True,'ok'); p.execute_authorized(); p.decide('payment-release',True,'ok'); p.execute_authorized()
 affected=p.revoke_bundle('vendor-risk','bank changed')
 assert {'activate','payments'} <= affected
 assert p.state.status['activate']==Status.ROLLED_BACK
 assert p.state.status['payments']==Status.ROLLED_BACK
 for safe in ['collect','tax_check','bank_check','draft','followup']:
  assert p.state.status[safe]==Status.EXECUTED

def test_no_model_can_self_authorize_without_decision():
 p=make(); p.execute_autonomous(); p.execute_authorized()
 assert p.state.status['activate']==Status.BLOCKED

def test_demo_end_to_end():
 r=run_demo(); assert r['before_correction']['payments']=='EXECUTED'; assert r['before_correction']['transmit']=='BLOCKED'; assert r['irreversible_transmission_executed'] is False; assert r['after_correction']['payments']=='ROLLED_BACK'

def test_strands_dependency_status_is_explicit():
 from authority_cut.strands_app import build_agent
 if importlib.util.find_spec('strands') is None:
  with pytest.raises(RuntimeError,match='not installed'):
   build_agent()
 else:
  assert build_agent() is not None

def test_rejected_human_decision_never_unlocks_authority():
 p=make(); p.execute_autonomous(); p.decide('vendor-risk',False,'not approved'); p.execute_authorized()
 assert p.state.status['activate']==Status.BLOCKED
 assert 'vendor_exception' not in p._grants()

def test_minimum_authority_cut_is_exact_over_policy_defined_bundles():
 from authority_cut.graph import ActionGraph
 from authority_cut.model import Action, DecisionBundle, Risk, RuntimeState
 actions=[Action('a','noop',risk=Risk.HUMAN,authorities=frozenset({'x'})),Action('b','noop',risk=Risk.HUMAN,authorities=frozenset({'y'})),Action('c','noop',risk=Risk.HUMAN,authorities=frozenset({'z'}))]
 bundles=[DecisionBundle('xy',frozenset({'x','y'}),'xy?',()),DecisionBundle('z',frozenset({'z'}),'z?',()),DecisionBundle('x',frozenset({'x'}),'x?',()),DecisionBundle('y',frozenset({'y'}),'y?',())]
 g=ActionGraph(actions,bundles); state=RuntimeState(status={x.action_id:Status.PENDING for x in actions})
 assert [b.bundle_id for b in g.minimum_authority_cut(state)]==['xy','z']

def test_uncovered_authority_fails_closed():
 from authority_cut.graph import ActionGraph
 from authority_cut.model import Action, Risk, RuntimeState
 g=ActionGraph([Action('a','noop',risk=Risk.HUMAN,authorities=frozenset({'missing'}))],[])
 with pytest.raises(ValueError,match='no decision bundles cover'):
  g.minimum_authority_cut(RuntimeState(status={'a':Status.PENDING}))

def test_irreversible_effect_is_not_falsely_reported_as_rolled_back():
 from authority_cut.graph import ActionGraph
 from authority_cut.model import Action, DecisionBundle, Risk
 class FakeTools:
  def execute(self,tool,payload): return {'executed':tool}
  def compensate(self,tool,payload): raise AssertionError('irreversible action must not be compensated')
 g=ActionGraph([Action('publish','publish',risk=Risk.HUMAN,authorities=frozenset({'publish'}),reversible=False)],[DecisionBundle('publish-auth',frozenset({'publish'}),'Publish?',('evidence-1',))])
 p=ControlPlane(g,FakeTools()); p.execute_autonomous(); p.decide('publish-auth',True,'approved'); p.execute_authorized()
 assert p.state.status['publish']==Status.EXECUTED
 affected=p.revoke_bundle('publish-auth','correction')
 assert affected=={'publish'}
 assert p.state.status['publish']==Status.BLOCKED

def test_api_controlled_judge_path():
 from fastapi.testclient import TestClient
 from authority_cut.api import app
 c=TestClient(app)
 assert c.get('/health').json()['status']=='READY'
 r=c.post('/api/reset'); assert r.status_code==200
 r=c.post('/api/run-safe').json(); assert r['status']['draft']=='EXECUTED' and r['status']['activate']=='BLOCKED'
 r=c.post('/api/decisions/vendor-risk',json={'approved':True,'rationale':'reviewed'}).json(); assert r['status']['activate']=='EXECUTED'
 r=c.post('/api/decisions/payment-release',json={'approved':True,'rationale':'reviewed'}).json(); assert r['status']['payments']=='EXECUTED'; assert r['status']['transmit']=='BLOCKED'
 r=c.post('/api/corrections/vendor-risk',json={'reason':'withdrawn'}).json(); assert 'activate' in r['affected'] and 'payments' in r['affected'] and 'transmit' in r['affected']; assert r['status']['payments']=='ROLLED_BACK'; assert r['status']['transmit']=='INVALIDATED'

def test_authority_cut_compresses_seven_protected_tool_effects_to_three_semantic_decisions():
 p=make(); p.execute_autonomous(); protected=[a for a in p.graph.actions.values() if a.authorities]
 assert len(protected)==7
 assert len(p.decision_surface())==3
 assert all(set(x['grants']) != {'vendor_exception','bank_change','payment_enable','funds_release'} for x in p.decision_surface())

def test_irreversible_funds_transfer_stays_blocked_without_distinct_funds_release():
 p=make(); p.execute_autonomous(); p.decide('vendor-risk',True,'approved'); p.execute_authorized(); p.decide('payment-release',True,'approved'); p.execute_authorized()
 assert p.state.status['remittance']==Status.EXECUTED
 assert p.state.status['transmit']==Status.BLOCKED
 assert {x['bundle_id'] for x in p.decision_surface()}=={'first-funds'}

def test_attention_and_safety_evaluation_contract():
 from authority_cut.evaluate import run_evaluation
 r=run_evaluation()
 assert r.protected_tool_effects==7
 assert r.authority_cut_decisions==3
 assert r.prompt_reduction_fraction==pytest.approx(4/7)
 assert r.safe_actions_before_human==5
 assert r.irreversible_effects_executed_without_funds_release==0
 assert r.unaffected_safe_actions_preserved==5
 assert r.reversible_effects_rolled_back_after_correction>=5

def test_future_decision_is_visible_but_cannot_be_approved_before_evidence_prerequisite():
 p=make(); p.execute_autonomous(); surface={x['bundle_id']:x for x in p.decision_surface()}
 assert surface['vendor-risk']['ready'] is True
 assert surface['payment-release']['ready'] is False
 assert surface['first-funds']['ready'] is False
 with pytest.raises(ValueError,match='first-funds.*not ready'):
  p.decide('first-funds',True,'premature approval')
 assert 'funds_release' not in p._grants()

def test_first_funds_becomes_ready_only_after_remittance_preview_exists():
 p=make(); p.execute_autonomous(); p.decide('vendor-risk',True,'approved'); p.execute_authorized(); p.decide('payment-release',True,'approved'); p.execute_authorized()
 surface={x['bundle_id']:x for x in p.decision_surface()}; assert surface['first-funds']['ready'] is True
 p.decide('first-funds',True,'reviewed irreversible release'); p.execute_authorized(); assert p.state.status['transmit']==Status.EXECUTED
 decision_receipt=next(r for r in p.state.receipts if r.get('human_decision')=='first-funds')
 assert decision_receipt['prereq_receipts']['remittance']['evidence']=='remittance-preview-42'

def test_api_rejects_premature_irreversible_approval():
 from fastapi.testclient import TestClient
 from authority_cut.api import app
 c=TestClient(app); c.post('/api/reset'); c.post('/api/run-safe')
 r=c.post('/api/decisions/first-funds',json={'approved':True,'rationale':'too early'})
 assert r.status_code==409
 assert 'not ready' in r.json()['detail']

def test_strands_model_toolset_cannot_issue_or_revoke_human_authority():
 from authority_cut.strands_app import STRANDS_TOOL_NAMES
 assert STRANDS_TOOL_NAMES==('execute_safe_vendor_work','get_authority_cut','execute_authorized_vendor_work')
 assert all('decision' not in name or name=='get_authority_cut' for name in STRANDS_TOOL_NAMES)
 assert all('revoke' not in name and 'approve' not in name for name in STRANDS_TOOL_NAMES)

def test_external_human_api_and_strands_adapter_share_exact_runtime_state():
 from authority_cut.runtime import get_plane
 from authority_cut.strands_app import execute_authorized_vendor_work, execute_safe_vendor_work
 p=get_plane(reset=True); execute_safe_vendor_work(); assert p.state.status['activate']==Status.BLOCKED
 p.decide('vendor-risk',True,'external principal approval'); execute_authorized_vendor_work(); assert p.state.status['activate']==Status.EXECUTED
 assert get_plane() is p

def test_judge_surface_exposes_truthful_runtime_state_and_evaluation():
 from fastapi.testclient import TestClient
 from authority_cut.api import app
 c=TestClient(app); html=c.get('/').text
 assert 'MODEL CANNOT APPROVE ITSELF' in html
 assert 'STRANDS RUNTIME UNVERIFIED' in html
 assert 'First-funds remains a distinct irreversible authority' in html
 r=c.get('/api/evaluation'); assert r.status_code==200
 assert r.json()['protected_tool_effects']==7
 assert r.json()['authority_cut_decisions']==3
