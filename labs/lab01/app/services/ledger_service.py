# ЛР1: заготовленный сервис. Допишите отмеченный метод и подключите объекты.
from decimal import Decimal, localcontext

from app.domain.ledger import LedgerEntry
from app.support.types import checked, currency, ensure_new_entry, Repository
from app.support.errors import DomainError

class LedgerService:
    def __init__(self, repository, rules=()):
        self._repository = repository
        self._rules = tuple(rules)

    def record(self, entry):
        if not isinstance(entry, LedgerEntry):
            raise DomainError("INVALID_ENTRY")

        ensure_new_entry(self._repository, entry.entry_id)

        for rule in self._rules:
            result = checked(rule(entry))
            if not result.allowed:
                raise DomainError(result.code)

        return self._repository.add(entry)

    def entries_for_transaction(self, transaction_id):
        return tuple(
            entry
            for entry in self._repository.all()
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
                Decimal("0.00"),
            )

    def record_debit(self, entry_id, transaction_id, account_id, amount):
        return self.record(
            LedgerEntry(entry_id, transaction_id, account_id, amount, "DEBIT")
        )

    def record_credit(self, entry_id, transaction_id, account_id, amount):
        return self.record(
            LedgerEntry(entry_id, transaction_id, account_id, amount, "CREDIT")
        )

def make_entity(
    entry_id,
    transaction_id,
    account_id,
    amount,
    entry_type,
    reverses_entry_id=None,
):
    return LedgerEntry(
        entry_id,
        transaction_id,
        account_id,
        amount,
        entry_type,
        reverses_entry_id,
    )

def view(entry):
    return {
        "entry_id": entry.entry_id,
        "transaction_id": entry.transaction_id,
        "account_id": entry.account_id,
        "amount": entry.amount,
        "entry_type": entry.entry_type,
        "reverses_entry_id": entry.reverses_entry_id,
    }

def invoke(service, method, *args):
    if method == "record":
        return service.record(args[0])

    if method == "entries_for_transaction":
        return service.entries_for_transaction(args[0])

    if method == "signed_total":
        return service.signed_total(*args)

    if method == "record_debit":
        return service.record_debit(*args)

    if method == "record_credit":
        return service.record_credit(*args)

    raise ValueError(method)

def new_service(repository=None):
    return LedgerService(
        repository
        if repository is not None
        else Repository("entry_id", "DUPLICATE_ENTRY")
    )
