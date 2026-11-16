from app.domain.posting_rules import PostingRule
from app.support.types import CheckResult

class LegacyPostingAdapter(PostingRule):
    def __init__(self, legacy):
        self._legacy = legacy

    def check(self, entry):
        if self._legacy.accepts(entry.entry_type, entry.amount.amount):
            return CheckResult(True)
        return CheckResult(False, "LEGACY_DENIED")