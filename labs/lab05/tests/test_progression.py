import pytest
from datetime import date, datetime, timezone
from decimal import Decimal
from app import api
from app.support.errors import DomainError


def code(expected, operation):
    with pytest.raises(DomainError) as caught:
        operation()
    assert caught.value.code == expected

from app.domain.ledger import LedgerEntry
from app.support.types import money

def test_progression_refused_entry_does_not_reserve_id():
    service = api.create()
    first = LedgerEntry("E1", "T", "ACC-1", money("10"), "DEBIT")
    service.record(first)
    code("ENTRY_AMOUNT_LIMIT", lambda: service.record(LedgerEntry("E2", "T", "ACC-1", money("1001"), "DEBIT")))
    assert service.entries_for_transaction("T") == (first,)
    second = LedgerEntry("E2", "T", "ACC-1", money("20"), "CREDIT")
    service.record(second)
    assert service.entries_for_transaction("T") == (first, second)
    assert service.signed_total("ACC-1", "EUR") == Decimal("10")

from app.domain.posting_rules import PostingRule
from app.services.ledger_service import LedgerService
from app.support.types import Repository, CheckResult

def test_progression_posting_dependency_error_does_not_consume_id():
    calls = []
    class Once(PostingRule):
        def check(self, item):
            calls.append(item)
            if len(calls) == 1: raise DomainError("TEMPORARY")
            return CheckResult(True)
    repo = Repository("entry_id", "DUPLICATE_ENTRY")
    rules = [Once()]
    service = LedgerService(repo, rules)
    rules.clear()
    entry = LedgerEntry("E", "T", "ACC-1", money("10"), "DEBIT")
    code("TEMPORARY", lambda: service.record(entry))
    assert len(calls) == 1 and repo.all() == ()
    service.record(entry)
    assert calls == [entry, entry] and repo.all() == (entry,)

from app.domain.ledger import LedgerEntry
from app.support.types import money, Repository
from app.services.ledger_service import LedgerService
from decimal import Decimal

def test_progression_extra_lab05():
    service = LedgerService(Repository("entry_id"), [])
    service.record(LedgerEntry("E1", "T", "A", money("20"), "DEBIT"))
    service.record(LedgerEntry("E2", "T", "A", money("30"), "CREDIT"))
    service.record(LedgerEntry("E3", "X", "B", money("10"), "CREDIT"))
    assert len(service.entries_for_account("A")) == 2
    assert service.transaction_summary("T", "EUR") == {"debit": Decimal("20"), "credit": Decimal("30"), "net": Decimal("10")}
    assert len(service._repository.all()) == 3
