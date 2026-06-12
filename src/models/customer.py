from src.models.account import Account


class Customer:
    """A customer who can hold one or more accounts.

    A customer is made up of Account objects (a "has-a" relationship), which is
    why this uses composition rather than inheritance.
    """

    def __init__(self, customer_id, name):
        if not name or not name.strip():
            raise ValueError("Customer name cannot be empty.")
        self._customer_id = customer_id
        self.name = name.strip()
        self._accounts = []

    @property
    def customer_id(self):
        return self._customer_id

    @property
    def accounts(self):
        return list(self._accounts)

    @property
    def total_balance(self):
        return sum(a.balance for a in self._accounts)

    def add_account(self, account):
        if not isinstance(account, Account):
            raise TypeError("Can only add Account objects.")
        if any(a.account_number == account.account_number for a in self._accounts):
            raise ValueError("Account already belongs to this customer.")
        self._accounts.append(account)

    def find_account(self, account_number):
        for a in self._accounts:
            if a.account_number == account_number:
                return a
        return None

    def to_dict(self):
        return {
            "customer_id": self._customer_id,
            "name": self.name,
            "accounts": [a.to_dict() for a in self._accounts],
        }

    @classmethod
    def from_dict(cls, data):
        customer = cls(data["customer_id"], data["name"])
        for acc_data in data.get("accounts", []):
            customer._accounts.append(Account.from_dict(acc_data))
        return customer

    def __str__(self):
        return f"Customer {self._customer_id} | {self.name} | {len(self._accounts)} account(s)"
