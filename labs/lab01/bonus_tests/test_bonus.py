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

def test_description():
    from app.domain.ledger import LedgerEntry
    assert LedgerEntry("E1","T","ACC-1",money("10"),"DEBIT").describe()=="E1:DEBIT:10.00:EUR"
