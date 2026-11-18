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

def test_credit_delegates(monkeypatch):
    service=api.create()
    calls=[]
    original=service.record
    def record(entry):
        calls.append(entry)
        return original(entry)
    monkeypatch.setattr(service,"record",record)
    service.record_credit("E","T","ACC-1",money("1"))
    assert len(calls)==1
