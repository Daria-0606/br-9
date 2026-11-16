from decimal import Decimal, localcontext
from app.domain.ledger import LedgerEntry
from app.domain.posting_rules import AllowedEntryTypeRule, MaximumEntryAmountRule
from app.support.types import checked, ensure_new_entry
from app.support.money import money, currency
from app.support.errors import DomainError

class LedgerService:
    def __init__(self, repository, rules=()):
        self._repository = repository
        self._rules = tuple(rules)

    def record(self, entry):
        if self._repository is None:
            raise DomainError("REPOSITORY_MISSING")
        ensure_new_entry(self._repository, entry.entry_id)
        for rule in self._rules:
            result = checked(rule.check(entry))
            if not result.allowed:
                raise DomainError(result.code)
        self._repository.add(entry)
        return entry

    def entries_for_transaction(self, transaction_id):
        return tuple(entry for entry in self._repository.all() if entry.transaction_id == transaction_id)

    def signed_total(self, account_id, code):
        currency(code)
        with localcontext() as ctx:
            ctx.prec = 28
            return sum((entry.signed_amount() for entry in self._repository.all()
                        if entry.account_id == account_id and entry.amount.currency == code), Decimal("0.00"))

    def record_debit(self, entry_id, transaction_id, account_id, amount):
        return self.record(LedgerEntry(entry_id, transaction_id, account_id, amount, "DEBIT"))

    def record_credit(self, entry_id, transaction_id, account_id, amount):
        return self.record(LedgerEntry(entry_id, transaction_id, account_id, amount, "CREDIT"))

    def entries_for_account(self, account_id):
        return tuple(entry for entry in self._repository.all() if entry.account_id == account_id)

    def transaction_summary(self, transaction_id, code):
        currency(code)
        debit = Decimal("0.00")
        credit = Decimal("0.00")
        with localcontext() as ctx:
            ctx.prec = 28
            for entry in self._repository.all():
                if entry.transaction_id != transaction_id or entry.amount.currency != code:
                    continue
                if entry.entry_type == "DEBIT":
                    debit += entry.amount.amount
                elif entry.entry_type == "CREDIT":
                    credit += entry.amount.amount
            net = credit - debit
        return {"debit": debit, "credit": credit, "net": net}

def make_entity(*args, **kwargs):
    return LedgerEntry(*args, **kwargs)

def invoke(service, method, *args, **kwargs):
    return getattr(service, method)(*args, **kwargs)

def view(entity):
    return {'entry_id': entity.entry_id, 'transaction_id': entity.transaction_id, 'account_id': entity.account_id, 'amount': entity.amount, 'entry_type': entity.entry_type, 'reverses_entry_id': entity.reverses_entry_id}
