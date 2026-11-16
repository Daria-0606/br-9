from app.services.ledger_service import LedgerService
from app.support.types import Repository
from app.support.money import money
from app.domain.posting_rules import AllowedEntryTypeRule, MaximumEntryAmountRule


def _default_rules():
    return (
        AllowedEntryTypeRule({"DEBIT", "CREDIT"}),
        MaximumEntryAmountRule(money("1000")),
    )


def build_service(repository=None, rules=None):
    if repository is None:
        repository = Repository("entry_id", "DUPLICATE_ENTRY")
    if rules is None:
        rules = _default_rules()
    return LedgerService(repository, rules)