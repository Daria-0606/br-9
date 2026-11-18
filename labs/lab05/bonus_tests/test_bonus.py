import pytest
from decimal import Decimal
from datetime import date, datetime, timezone, timedelta
from app import api
from app.support.errors import DomainError
from app.support.types import Repository, CheckResult, Money, money


def error(code, operation):
    with pytest.raises(DomainError) as caught:
        operation()
    assert caught.value.code == code


def invoke(service, method, *args, **kwargs):
    return api.call(service, method, *args, **kwargs)

def test_legacy_posting():
    from app.domain.ledger import LedgerEntry
    from app.domain.adapters import LegacyPostingAdapter
    class Legacy:
        def accepts(self,kind,amount):return kind=="DEBIT" and amount<=10
    assert not LegacyPostingAdapter(Legacy()).check(LedgerEntry("E","T","ACC-1",money("20"),"DEBIT")).allowed
