from datetime import datetime


class Transaction:
    """One record of money moving in or out of an account.

    A transaction never changes once it is created, so all of its fields are
    read-only.
    """

    VALID_TYPES = ("deposit", "withdraw", "transfer_in", "transfer_out")

    def __init__(self, kind, amount, balance_after, timestamp=None, note=""):
        if kind not in self.VALID_TYPES:
            raise ValueError(f"Unknown transaction type: {kind!r}")
        if amount <= 0:
            raise ValueError("Transaction amount must be positive.")

        self._kind = kind
        self._amount = float(amount)
        self._balance_after = float(balance_after)
        self._timestamp = timestamp or datetime.now().isoformat(timespec="seconds")
        self._note = note

    @property
    def kind(self):
        return self._kind

    @property
    def amount(self):
        return self._amount

    @property
    def balance_after(self):
        return self._balance_after

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def note(self):
        return self._note

    def to_dict(self):
        return {
            "kind": self._kind,
            "amount": self._amount,
            "balance_after": self._balance_after,
            "timestamp": self._timestamp,
            "note": self._note,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            kind=data["kind"],
            amount=data["amount"],
            balance_after=data["balance_after"],
            timestamp=data.get("timestamp"),
            note=data.get("note", ""),
        )

    def __str__(self):
        return f"[{self._timestamp}] {self._kind} {self._amount:.2f} -> balance {self._balance_after:.2f}"
