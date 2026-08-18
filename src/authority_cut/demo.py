from .engine import ControlPlane
from .tools import VendorTools
from .workflow import vendor_onboarding_graph


def run_demo():
    p = ControlPlane(vendor_onboarding_graph(), VendorTools.memory())
    p.execute_autonomous()
    surface = p.decision_surface()
    p.decide('vendor-risk', True, 'Human verified bundled exception evidence')
    p.execute_authorized()
    after_vendor = p.decision_surface()
    p.decide('payment-release', True, 'Human authorizes payment profile and terms')
    p.execute_authorized()
    before = {k: v.value for k, v in p.state.status.items()}
    # `first-funds` is deliberately not approved: the irreversible transmission stays blocked.
    affected = p.revoke_bundle(
        'vendor-risk',
        'Principal withdraws the previously granted vendor-risk authority',
    )
    after = {k: v.value for k, v in p.state.status.items()}
    return {
        'initial_decision_surface': surface,
        'after_vendor_decision_surface': after_vendor,
        'before_correction': before,
        'affected_by_correction': sorted(affected),
        'after_correction': after,
        'irreversible_transmission_executed': before['transmit'] == 'EXECUTED',
        'receipts': p.state.receipts,
    }
