"""Acceptance probe for the deployable public Strands judge surface."""
from fastapi.testclient import TestClient
from authority_cut.public_app import app

c = TestClient(app)
health = c.get('/health')
assert health.status_code == 200
h = health.json()
assert h['status'] == 'READY'
assert h['live_strands_agent_loop'] == 'AVAILABLE'
assert h['foundation_model'] == 'UNVERIFIED'
assert h['agentcore'] == 'UNVERIFIED'
assert h['authority_mutation_tools'] == []

boundary = c.get('/api/tool-boundary')
assert boundary.status_code == 200
assert boundary.json()['authority_mutation_tools'] == []

proof = c.post('/api/strands-proof')
assert proof.status_code == 200
p = proof.json()
assert p['execution'] == 'REAL_STRANDS_AGENT_LOOP_DETERMINISTIC_MODEL'
assert p['authority_mutation_tools'] == []
assert p['safe_actions_preserved'] == 5
assert p['protected_reversible_effects_rolled_back'] == 6
assert p['irreversible_transmit_after_correction'] == 'INVALIDATED'
assert p['foundation_model_invocation'] == 'UNVERIFIED'
assert p['agentcore'] == 'UNVERIFIED'
assert len(p['phases']) == 4
print('PUBLIC_STRANDS_SURFACE=PASS')
