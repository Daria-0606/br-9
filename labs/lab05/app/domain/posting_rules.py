from abc import ABC, abstractmethod
from app.support.types import CheckResult
from app.support.errors import DomainError


class PostingRule(ABC):
    @abstractmethod
    def check(self, entry):
        pass


class AllowedEntryTypeRule(PostingRule):
    def __init__(self, types):
        self._types = frozenset(types)

    def check(self, entry):
        if entry.entry_type in self._types:
            return CheckResult(True)
        return CheckResult(False, "ENTRY_TYPE_DENIED")


class MaximumEntryAmountRule(PostingRule):
    def __init__(self, maximum):
        self._maximum = maximum

    def check(self, entry):
        if entry.amount.currency != self._maximum.currency:
            raise DomainError("CURRENCY_MISMATCH")
        if entry.amount.amount <= self._maximum.amount:
            return CheckResult(True)
        return CheckResult(False, "ENTRY_AMOUNT_LIMIT")