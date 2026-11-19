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
