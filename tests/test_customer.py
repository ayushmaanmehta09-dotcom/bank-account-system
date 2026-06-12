"""Tests for the Customer model (composition of accounts)."""

import pytest

from src.models.account import Account
from src.models.customer import Customer


def test_customer_requires_a_name():
    with pytest.raises(ValueError):
        Customer(1, "   ")


def test_add_account_and_total_balance():
    cust = Customer(1, "Ayushmaan")
    cust.add_account(Account(1001, "Ayushmaan", 100))
    cust.add_account(Account(1002, "Ayushmaan", 50))
    assert len(cust.accounts) == 2
    assert cust.total_balance == 150


def test_cannot_add_same_account_twice():
    cust = Customer(1, "Ayushmaan")
    acc = Account(1001, "Ayushmaan", 100)
    cust.add_account(acc)
    with pytest.raises(ValueError):
        cust.add_account(acc)


def test_add_account_rejects_wrong_type():
    cust = Customer(1, "Ayushmaan")
    with pytest.raises(TypeError):
        cust.add_account("not an account")


def test_accounts_returns_a_copy():
    cust = Customer(1, "Ayushmaan")
    cust.accounts.append("FAKE")
    assert cust.accounts == []


def test_find_account():
    cust = Customer(1, "Ayushmaan")
    cust.add_account(Account(1001, "Ayushmaan", 100))
    assert cust.find_account(1001) is not None
    assert cust.find_account(9999) is None


def test_customer_round_trips_through_dict():
    cust = Customer(1, "Ayushmaan")
    cust.add_account(Account(1001, "Ayushmaan", 100))
    restored = Customer.from_dict(cust.to_dict())
    assert restored.name == "Ayushmaan"
    assert restored.total_balance == 100
