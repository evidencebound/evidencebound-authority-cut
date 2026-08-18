from __future__ import annotations
from .graph import ActionGraph
from .model import Action, DecisionBundle, Risk


def vendor_onboarding_graph() -> ActionGraph:
    actions = [
        Action('collect', 'collect_vendor_record'),
        Action('tax_check', 'validate_tax_id', ('collect',)),
        Action('bank_check', 'validate_bank', ('collect',)),
        Action('draft', 'create_draft_vendor', ('tax_check', 'bank_check')),
        Action('followup', 'schedule_followup', ('draft',), reversible=True),
        Action('activate','activate_vendor',('draft',),Risk.HUMAN,frozenset({'vendor_exception','bank_change'}),True),
        Action('erp_sync','sync_vendor_to_erp',('activate',),Risk.HUMAN,frozenset({'vendor_exception'}),True),
        Action('purchasing','open_purchase_channel',('activate',),Risk.HUMAN,frozenset({'vendor_exception'}),True),
        Action('payments','enable_payments',('activate',),Risk.HIGH,frozenset({'payment_enable'}),True),
        Action('terms','set_payment_terms',('payments',),Risk.HUMAN,frozenset({'payment_enable'}),True),
        Action('remittance','prepare_remittance_profile',('terms',),Risk.HUMAN,frozenset({'payment_enable'}),True),
        Action('transmit','transmit_first_payment',('remittance',),Risk.HIGH,frozenset({'funds_release'}),False),
    ]
    bundles = [
        DecisionBundle('vendor-risk',frozenset({'vendor_exception','bank_change'}),'Approve the reviewed vendor identity/tax exception and new bank account?',('tax-check-42','bank-check-42'),('tax_check','bank_check')),
        DecisionBundle('payment-release',frozenset({'payment_enable'}),'Enable the vendor payment profile and terms?',('draft-vendor-record','bank-check-42'),('activate',)),
        DecisionBundle('first-funds',frozenset({'funds_release'}),'Release the first irreversible payment transmission?',('payment-profile-42','remittance-preview-42'),('remittance',)),
    ]
    return ActionGraph(actions,bundles)
