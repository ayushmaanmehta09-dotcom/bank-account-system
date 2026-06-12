from src.models.account import Account
from src.models.customer import Customer
from src.persistence.storage import JsonStorage


class BankService:
    """The layer the web app talks to.

    It holds all the customers and accounts, hands out new IDs, runs the
    operations that involve more than one account (like transfers), and saves
    to disk after every change. The web routes only ever call this class, so
    they don't need to know how accounts work or how the data is stored.
    """

    def __init__(self, storage=None):
        self._storage = storage or JsonStorage()
        self._customers = []
        self._next_customer_id = 1
        self._next_account_number = 1001
        self.load()

    @property
    def customers(self):
        return list(self._customers)

    def all_accounts(self):
        return [acc for cust in self._customers for acc in cust.accounts]

    def find_customer(self, customer_id):
        for c in self._customers:
            if c.customer_id == customer_id:
                return c
        return None

    def find_account(self, account_number):
        for c in self._customers:
            acc = c.find_account(account_number)
            if acc is not None:
                return acc
        return None

    def create_customer(self, name):
        customer = Customer(self._next_customer_id, name)
        self._customers.append(customer)
        self._next_customer_id += 1
        self.save()
        return customer

    def open_account(self, customer_id, opening_balance=0.0):
        customer = self.find_customer(customer_id)
        if customer is None:
            raise ValueError("No such customer.")
        account = Account(self._next_account_number, customer.name, opening_balance)
        customer.add_account(account)
        self._next_account_number += 1
        self.save()
        return account

    def deposit(self, account_number, amount):
        account = self._require_account(account_number)
        account.deposit(amount)
        self.save()
        return account

    def withdraw(self, account_number, amount):
        account = self._require_account(account_number)
        account.withdraw(amount)
        self.save()
        return account

    def transfer(self, from_number, to_number, amount):
        if from_number == to_number:
            raise ValueError("Cannot transfer to the same account.")
        source = self._require_account(from_number)
        target = self._require_account(to_number)
        # Take the money out first. If the source doesn't have enough, this
        # raises before anything is added to the target, so no money is lost.
        source.transfer_out(amount, note=f"to {to_number}")
        target.transfer_in(amount, note=f"from {from_number}")
        self.save()
        return source, target

    def _require_account(self, account_number):
        account = self.find_account(account_number)
        if account is None:
            raise ValueError(f"No account numbered {account_number}.")
        return account

    def save(self):
        self._storage.save(self._customers)

    def load(self):
        data = self._storage.load()
        self._customers = [Customer.from_dict(c) for c in data.get("customers", [])]
        # Carry on numbering from whatever is already saved so new IDs don't
        # clash with existing ones.
        if self._customers:
            self._next_customer_id = max(c.customer_id for c in self._customers) + 1
            existing_accounts = [a.account_number for a in self.all_accounts()]
            if existing_accounts:
                self._next_account_number = max(existing_accounts) + 1
