"""Tests for the BankService (business logic + persistence).

These use a temporary JSON file via pytest's tmp_path fixture, so they never
touch the real bank_data.json.
"""

import pytest

from src.persistence.storage import JsonStorage
from src.services.bank_service import BankService


def make_service(tmp_path):
    storage = JsonStorage(str(tmp_path / "test_bank.json"))
    return BankService(storage)


def test_create_customer_and_open_account(tmp_path):
    bank = make_service(tmp_path)
    cust = bank.create_customer("Ayushmaan")
    acc = bank.open_account(cust.customer_id, 100)
    assert acc.balance == 100
    assert bank.find_account(acc.account_number) is acc


def test_deposit_and_withdraw_through_service(tmp_path):
    bank = make_service(tmp_path)
    cust = bank.create_customer("Ayushmaan")
    acc = bank.open_account(cust.customer_id, 100)
    bank.deposit(acc.account_number, 50)
    bank.withdraw(acc.account_number, 30)
    assert acc.balance == 120


def test_transfer_moves_money_between_accounts(tmp_path):
    bank = make_service(tmp_path)
    cust = bank.create_customer("Ayushmaan")
    a = bank.open_account(cust.customer_id, 100)
    b = bank.open_account(cust.customer_id, 0)
    bank.transfer(a.account_number, b.account_number, 40)
    assert a.balance == 60
    assert b.balance == 40


def test_transfer_with_insufficient_funds_leaves_balances_unchanged(tmp_path):
    bank = make_service(tmp_path)
    cust = bank.create_customer("Ayushmaan")
    a = bank.open_account(cust.customer_id, 30)
    b = bank.open_account(cust.customer_id, 0)
    with pytest.raises(ValueError):
        bank.transfer(a.account_number, b.account_number, 100)
    assert a.balance == 30          # nothing left the source
    assert b.balance == 0           # nothing reached the target


def test_cannot_transfer_to_same_account(tmp_path):
    bank = make_service(tmp_path)
    cust = bank.create_customer("Ayushmaan")
    a = bank.open_account(cust.customer_id, 100)
    with pytest.raises(ValueError):
        bank.transfer(a.account_number, a.account_number, 10)


def test_operations_on_missing_account_raise(tmp_path):
    bank = make_service(tmp_path)
    with pytest.raises(ValueError):
        bank.deposit(9999, 10)


def test_data_persists_across_reloads(tmp_path):
    path = tmp_path / "test_bank.json"
    bank = BankService(JsonStorage(str(path)))
    cust = bank.create_customer("Ayushmaan")
    acc = bank.open_account(cust.customer_id, 200)
    acc_number = acc.account_number

    # A brand-new service pointed at the same file must see the saved data.
    reloaded = BankService(JsonStorage(str(path)))
    found = reloaded.find_account(acc_number)
    assert found is not None
    assert found.balance == 200


def test_ids_do_not_collide_after_reload(tmp_path):
    path = tmp_path / "test_bank.json"
    bank = BankService(JsonStorage(str(path)))
    c1 = bank.create_customer("Ayushmaan")
    bank.open_account(c1.customer_id, 10)

    reloaded = BankService(JsonStorage(str(path)))
    c2 = reloaded.create_customer("Bob")
    assert c2.customer_id != c1.customer_id      # new id, no collision
