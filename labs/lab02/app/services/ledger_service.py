from decimal import Decimal, localcontext

from app.domain.ledger import LedgerEntry
from app.support.errors import DomainError
from app.support.types import (
    Repository,
    checked,
    currency,
    ensure_new_entry,
    money,
)


class LedgerService:
    def __init__(self, repository, rules=()):
        self._repository = repository
        self._rules = tuple(rules)

    def record(self, entry):
        ensure_new_entry(self._repository, entry.entry_id)
        entry.amount.same_currency(money("1000"))

        if entry.amount.amount > 1000:
            raise DomainError("ENTRY_AMOUNT_LIMIT")

        return self._repository.add(entry)

    def entries_for_transaction(self, transaction_id):
        return tuple(
            entry
            for entry in self._repository.all()
            if entry.transaction_id == transaction_id
        )

    def entries_for_account(self, account_id, code):
        currency(code)

        return tuple(
            entry
            for entry in self._repository.all()
            if entry.account_id == account_id
            and entry.amount.currency == code
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

    def record_debit(
        self,
        entry_id,
        transaction_id,
        account_id,
        amount,
    ):
        return self.record(
            LedgerEntry(
                entry_id,
                transaction_id,
                account_id,
                amount,
                "DEBIT",
            )
        )

    def record_credit(
        self,
        entry_id,
        transaction_id,
        account_id,
        amount,
    ):
        return self.record(
            LedgerEntry(
                entry_id,
                transaction_id,
                account_id,
                amount,
                "CREDIT",
            )
        )


def make_entity(*args, **kwargs):
    return LedgerEntry(*args, **kwargs)


def invoke(service, method, *args, **kwargs):
    return getattr(service, method)(*args, **kwargs)


def view(entity):
    return {
        "entry_id": entity.entry_id,
        "transaction_id": entity.transaction_id,
        "account_id": entity.account_id,
        "amount": entity.amount,
        "entry_type": entity.entry_type,
        "reverses_entry_id": entity.reverses_entry_id,
    }


def new_service(repository=None):
    return LedgerService(
        repository
        if repository is not None
        else Repository("entry_id", "DUPLICATE_ENTRY")
    )
