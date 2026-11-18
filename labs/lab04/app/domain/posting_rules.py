from abc import ABC, abstractmethod
from app.support.types import CheckResult, Money, choice, result_code
from app.support.errors import DomainError


class PostingRule(ABC):
    @abstractmethod
    def check(self, entry):
        raise NotImplementedError


class AllowedEntryTypeRule(PostingRule):
    def __init__(self, types):
        self._types = frozenset(types)
        for value in self._types:
            choice(value, ("DEBIT", "CREDIT"), "INVALID_CONFIG")

    def check(self, entry):
        if entry.entry_type not in self._types:
            return CheckResult(False, "ENTRY_TYPE_DENIED")
        return CheckResult(True)


class MaximumEntryAmountRule(PostingRule):
    def __init__(self, maximum):
        if not isinstance(maximum, Money):
            raise DomainError("INVALID_CONFIG")
        self._maximum = maximum

    def check(self, entry):
        entry.amount.same_currency(self._maximum)
        if entry.amount.amount > self._maximum.amount:
            return CheckResult(False, "ENTRY_AMOUNT_LIMIT")
        return CheckResult(True)
