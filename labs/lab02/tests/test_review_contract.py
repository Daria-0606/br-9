import pytest
from decimal import Decimal
from datetime import date, datetime, timezone, timedelta
from app import api
from app.support.errors import DomainError


def assert_code(code, action):
    with pytest.raises(DomainError) as caught:
        action()
    assert caught.value.code == code

from app.support.types import money

def test_review_totals_filter_currency_and_empty_account():
    from app.support.types import Repository
    from app.domain.ledger import LedgerEntry
    repo=Repository("entry_id","DUPLICATE_ENTRY")
    repo.add(LedgerEntry("E1","T","ACC-1",money("10"),"DEBIT"))
    repo.add(LedgerEntry("E2","T","ACC-1",money("3","USD"),"CREDIT"))
    service=api.create(repository=repo)
    assert service.signed_total("ACC-1","EUR") == Decimal("-10")
    assert service.signed_total("ACC-1","USD") == Decimal("3")
    assert service.signed_total("OTHER","EUR") == Decimal("0.00")
