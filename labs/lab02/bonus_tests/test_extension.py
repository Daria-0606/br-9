from app import api
from app.support.errors import DomainError
from app.support.types import money
from decimal import Decimal
import pytest

def error(code, action):
    with pytest.raises(DomainError) as exc:
        action()
    assert exc.value.code == code

from app.domain.ledger import LedgerEntry

def test_bonus_account_entries_filter_and_keep_insertion_order():
    service = api.create()
    assert hasattr(service, "entries_for_account"), "Реализуйте бонусную выборку entries_for_account"
    # USD помещаем напрямую в готовый repository: стандартная денежная политика — EUR.
    from app.support.types import Repository
    repository = Repository("entry_id", "DUPLICATE_ENTRY")
    entries = [LedgerEntry("E2", "T", "A", money("2"), "DEBIT"),
               LedgerEntry("E1", "T", "A", money("1"), "CREDIT"),
               LedgerEntry("E3", "T", "B", money("3"), "DEBIT"),
               LedgerEntry("E4", "T", "A", money("4", "USD"), "CREDIT")]
    for entry in entries: repository.add(entry)
    service = api.create(repository=repository)
    result = service.entries_for_account("A", "EUR")
    assert result == tuple(entries[:2]) and type(result) is tuple
    assert result[0] is entries[0]
    assert service.entries_for_account("A", "USD") == (entries[3],)
    assert service.entries_for_account("UNKNOWN", "EUR") == ()
    error("INVALID_CURRENCY", lambda: service.entries_for_account("A", "XXX"))
    assert repository.all() == tuple(entries)
    repository.add(LedgerEntry("E5", "T", "A", money("5"), "DEBIT"))
    assert result == tuple(entries[:2])  # Уже возвращённая выборка не расширилась.
