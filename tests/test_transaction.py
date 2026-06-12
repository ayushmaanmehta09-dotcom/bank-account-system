"""Tests for the Transaction model (immutability + validation)."""

import pytest

from src.models.transaction import Transaction


def test_transaction_stores_values():
    t = Transaction("deposit", 100, 100)
    assert t.kind == "deposit"
    assert t.amount == 100
    assert t.balance_after == 100


def test_transaction_rejects_unknown_kind():
    with pytest.raises(ValueError):
        Transaction("magic", 100, 100)


def test_transaction_rejects_non_positive_amount():
    with pytest.raises(ValueError):
        Transaction("deposit", 0, 0)


def test_transaction_is_read_only():
    t = Transaction("deposit", 50, 50)
    with pytest.raises(AttributeError):
        t.amount = 999          # no setter exists -> encapsulation holds


def test_transaction_round_trips_through_dict():
    t = Transaction("withdraw", 25, 75, note="rent")
    restored = Transaction.from_dict(t.to_dict())
    assert restored.kind == "withdraw"
    assert restored.amount == 25
    assert restored.balance_after == 75
    assert restored.note == "rent"
