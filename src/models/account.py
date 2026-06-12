from src.models.transaction import Transaction


class Account:
    """A bank account that keeps control of its own balance.

    The balance is kept in a private attribute and can only be read, never set
    directly. The only way to change it is through deposit() and withdraw(),
    which both check the amount first. That way the balance can never become
    negative or be set to a random value from outside.
    """

    def __init__(self, account_number, owner, balance=0.0):
        self._account_number = account_number
        self.owner = owner
        self._balance = 0.0
        self._transactions = []
        if balance > 0:
            # Send the opening amount through deposit() so it gets validated
            # and recorded like any other deposit.
            self.deposit(balance, note="Opening balance")

    @property
    def account_number(self):
        return self._account_number

    @property
    def balance(self):
        return self._balance

    @property
    def transactions(self):
        # Hand back a copy so the caller can't edit our real history list.
        return list(self._transactions)

    def deposit(self, amount, note=""):
        amount = self._validate_amount(amount)
        self._balance += amount
        self._transactions.append(
            Transaction("deposit", amount, self._balance, note=note)
        )

    def withdraw(self, amount, note=""):
        amount = self._validate_amount(amount)
        if amount > self._balance:
            raise ValueError("Insufficient funds.")
        self._balance -= amount
        self._transactions.append(
            Transaction("withdraw", amount, self._balance, note=note)
        )

    def transfer_out(self, amount, note=""):
        # Money leaving this account as part of a transfer.
        amount = self._validate_amount(amount)
        if amount > self._balance:
            raise ValueError("Insufficient funds.")
        self._balance -= amount
        self._transactions.append(
            Transaction("transfer_out", amount, self._balance, note=note)
        )

    def transfer_in(self, amount, note=""):
        # Money arriving in this account as part of a transfer.
        amount = self._validate_amount(amount)
        self._balance += amount
        self._transactions.append(
            Transaction("transfer_in", amount, self._balance, note=note)
        )

    @staticmethod
    def _validate_amount(amount):
        # bool is technically an int in Python, so check for it explicitly.
        if isinstance(amount, bool) or not isinstance(amount, (int, float)):
            raise ValueError("Amount must be a number.")
        if amount <= 0:
            raise ValueError("Amount must be a positive number.")
        return float(amount)

    def to_dict(self):
        return {
            "account_number": self._account_number,
            "owner": self.owner,
            "balance": self._balance,
            "transactions": [t.to_dict() for t in self._transactions],
        }

    @classmethod
    def from_dict(cls, data):
        # Restore the saved state directly instead of replaying deposits,
        # otherwise we'd create duplicate transaction records.
        account = cls(data["account_number"], data["owner"], balance=0.0)
        account._balance = float(data["balance"])
        account._transactions = [Transaction.from_dict(t) for t in data.get("transactions", [])]
        return account

    def __str__(self):
        return f"Account {self._account_number} | {self.owner} | balance {self._balance:.2f}"
