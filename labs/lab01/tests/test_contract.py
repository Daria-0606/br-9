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

def entry(key="E1",amount="10",kind="DEBIT",account="ACC-1",transaction="TX-1",code="EUR"):
    return api.make(key,transaction,account,money(amount,code),kind)

def test_signed_journal_and_order():
    service=api.create()
    first=entry()
    invoke(service,"record",first)
    second=entry("E2","3","CREDIT")
    invoke(service,"record",second)
    invoke(service,"record",entry("E3","90",account="ACC-2",transaction="TX-2"))
    assert invoke(service,"signed_total","ACC-1","EUR")==Decimal("-7")
    assert invoke(service,"entries_for_transaction","TX-1")== (first,second)

def test_empty_and_independent_repository():
    service=api.create()
    invoke(service,"record",entry())
    assert invoke(api.create(),"entries_for_transaction","TX-1")==()
