# ЛР1: заготовленный сервис. Допишите отмеченный метод и подключите объекты.
from decimal import Decimal, localcontext


from app.domain.ledger import LedgerEntry


from app.support.types import checked, money, currency, ensure_new_entry


from app.support.errors import DomainError


class LedgerService:
    def __init__(self, repository, rules=()):
        self._repository = repository
        self._rules = tuple(rules)

    def record(self, entry):
        raise NotImplementedError("ЛР1: завершите LedgerService.record")

    def entries_for_transaction(self, transaction_id):
        return tuple(entry for entry in self._repository.all() if entry.transaction_id == transaction_id)

    def signed_total(self, account_id, code):
        currency(code)
        with localcontext() as ctx:
            ctx.prec = 28
            return sum((entry.signed_amount() for entry in self._repository.all()
                        if entry.account_id == account_id and entry.amount.currency == code), Decimal("0.00"))

    def record_debit(self, entry_id, transaction_id, account_id, amount):
        return self.record(LedgerEntry(entry_id, transaction_id, account_id, amount, "DEBIT"))

    def record_credit(self, entry_id, transaction_id, account_id, amount):
        return self.record(LedgerEntry(entry_id, transaction_id, account_id, amount, "CREDIT"))


from app.support.types import Repository, money


# Ниже — прежний рабочий путь. Перенесите поведение, затем обновите
# make_entity, invoke, view и new_service: сигнатуры должны сохраниться.
from decimal import Decimal
from app.support.errors import DomainError


def make_entity(entry_id,transaction_id,account_id,amount,entry_type,reverses_entry_id=None):
    return dict(entry_id=entry_id,transaction_id=transaction_id,account_id=account_id,amount=amount,entry_type=entry_type,reverses_entry_id=reverses_entry_id)


def _new_legacy_service(repository):return {"repository":repository}

def view(entry):return dict(entry)


def invoke(service,method,*args):
    repository=service["repository"]
    if method=="record":return repository.add(args[0])
    if method=="entries_for_transaction":return tuple(e for e in repository.all() if e["transaction_id"]==args[0])
    if method=="signed_total":
        account_id,code=args
        return sum((-e["amount"].amount if e["entry_type"]=="DEBIT" else e["amount"].amount
                    for e in repository.all() if e["account_id"]==account_id and e["amount"].currency==code),Decimal("0.00"))
    raise ValueError(method)


from app.support.types import Repository

def new_service(repository=None):
    return _new_legacy_service(repository if repository is not None else Repository("entry_id","DUPLICATE_ENTRY"))
