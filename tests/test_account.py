"""Tests for the Account model — the core encapsulation guarantees."""

import pytest

from src.models.account import Account


def test_new_account_starts_empty():
    acc = Account(1001, "Ayushmaan")
    assert acc.account_number == 1001
    assert acc.owner == "Ayushmaan"
    assert acc.balance == 0


def test_opening_balance_is_recorded_as_transaction():
    acc = Account(1001, "Ayushmaan", 100)
    assert acc.balance == 100
    assert len(acc.transactions) == 1
    assert acc.transactions[0].kind == "deposit"


def test_deposit_increases_balance():
    acc = Account(1001, "Ayushmaan")
    acc.deposit(50)
    assert acc.balance == 50


def test_withdraw_decreases_balance():
    acc = Account(1001, "Ayushmaan", 100)
    acc.withdraw(40)
    assert acc.balance == 60


def test_balance_is_read_only():
    acc = Account(1001, "Ayushmaan", 100)
    with pytest.raises(AttributeError):
        acc.balance = 999999            # no setter -> cannot be forced


def test_account_number_is_read_only():
    acc = Account(1001, "Ayushmaan")
    with pytest.raises(AttributeError):
        acc.account_number = 2002


def test_deposit_rejects_non_positive():
    acc = Account(1001, "Ayushmaan")
    with pytest.raises(ValueError):
        acc.deposit(-10)
    with pytest.raises(ValueError):
        acc.deposit(0)


def test_deposit_rejects_booleans():
    # bool is a subclass of int in Python; the guard must still reject it.
    acc = Account(1001, "Ayushmaan")
    with pytest.raises(ValueError):
        acc.deposit(True)


def test_overdraw_is_blocked_and_balance_unchanged():
    acc = Account(1001, "Ayushmaan", 50)
    with pytest.raises(ValueError):
        acc.withdraw(100)
    assert acc.balance == 50            # the invariant held after a failed attempt


def test_transactions_returns_a_copy():
    acc = Account(1001, "Ayushmaan", 100)
    acc.transactions.append("FAKE")
    assert all(t != "FAKE" for t in acc.transactions)


def test_account_round_trips_through_dict():
    acc = Account(1001, "Ayushmaan", 100)
    acc.withdraw(30)
    restored = Account.from_dict(acc.to_dict())
    assert restored.account_number == 1001
    assert restored.balance == 70
    assert len(restored.transactions) == 2   # opening deposit + withdrawal
