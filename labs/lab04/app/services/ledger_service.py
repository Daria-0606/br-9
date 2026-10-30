
from decimal import Decimal, localcontext
from app.domain.ledger import LedgerEntry
from app.domain.posting_rules import AllowedEntryTypeRule, MaximumEntryAmountRule
from app.support.types import checked, money, currency, ensure_new_entry
from app.support.errors import DomainError


class LedgerService:
    def __init__(self, repository, rules=()):
        self._repository = repository
        self._rules = [
            AllowedEntryTypeRule({"DEBIT", "CREDIT"}),
            MaximumEntryAmountRule(money("1000"))
        ]

    def record(self, entry):
        ensure_new_entry(self._repository, entry.entry_id)
        for rule in self._rules:
            result = checked(rule.check(entry))
            if not result.allowed:
                raise DomainError(result.code)
        return self._repository.add(entry)

    def entries_for_transaction(self, transaction_id):
        return tuple(
            entry for entry in self._repository.all()
            if entry.transaction_id == transaction_id
        )

    def signed_total(self, account_id, code):
        currency(code)
        with localcontext() as ctx:
            ctx.prec = 28
            return sum(
                (
                    entry.signed_amount()
                    for entry in self._repository.all()
                    if entry.account_id == account_id
                    and entry.amount.currency == code
                ),
                Decimal("0.00")
            )

    def record_debit(self, entry_id, transaction_id, account_id, amount):
        entry = LedgerEntry(
            entry_id, transaction_id, account_id, amount, "DEBIT"
        )
        return self.record(entry)

    def record_credit(self, entry_id, transaction_id, account_id, amount):
        entry = LedgerEntry(entry_id, transaction_id, account_id, amount, "CREDIT")
        return self.record(entry)


def make_entity(*args, **kwargs):
    return LedgerEntry(*args, **kwargs)


def invoke(service, method, *args, **kwargs):
    return getattr(service, method)(*args, **kwargs)


def view(entity):
    return {
        'entry_id': entity.entry_id,
        'transaction_id': entity.transaction_id,
        'account_id': entity.account_id,
        'amount': entity.amount,
        'entry_type': entity.entry_type,
        'reverses_entry_id': entity.reverses_entry_id
    }


from app.support.types import Repository, money


def new_service(repository=None):
    return LedgerService(
        repository if repository is not None
        else Repository("entry_id", "DUPLICATE_ENTRY")
    )
