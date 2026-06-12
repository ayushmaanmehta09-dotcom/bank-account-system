# Bank Account System

A small banking app built for the Programming Lab project. It started as a
single Bank Account class about encapsulation, and I extended it into a proper
multi-class system with a web interface and saved data.

You can create customers, open accounts for them, and deposit, withdraw, or
transfer money. Every account keeps its own transaction history, and all the
data is saved to a JSON file so it's still there after you restart.

## Main idea: encapsulation

The point of the project is that an account protects its own balance:

- `_balance` is private and only exposed through a read-only property, so you
  can read `account.balance` but you can't do `account.balance = 999`.
- The only way to change the money is `deposit()` and `withdraw()`, which check
  the amount first.
- The rule "you can't withdraw more than you have" lives in one place, so it
  can't be skipped.

On top of that, a `Customer` is built out of `Account` objects (composition),
and each `Transaction` is a record that can't be changed after it's made.

## Folder structure

```
Programming Lab/
├── main.py                 # starts the web app
├── requirements.txt        # Flask and pytest
├── bank_data.json          # the saved data (created when you run it)
├── src/
│   ├── models/
│   │   ├── account.py
│   │   ├── customer.py
│   │   └── transaction.py
│   ├── services/
│   │   └── bank_service.py # the logic the web layer calls
│   ├── persistence/
│   │   └── storage.py      # loads/saves the JSON file
│   └── ui/
│       ├── app.py          # Flask routes
│       ├── templates/      # the HTML pages
│       └── static/         # the CSS
└── tests/                  # pytest tests for each part
```

The web routes only talk to `BankService`, and `BankService` is the only thing
that talks to the models and the storage. So the rules stay in one place and the
interface could be swapped out without touching them.

## Running it

```bash
python3 -m pip install -r requirements.txt
python3 main.py
```

Then open http://127.0.0.1:5000 in a browser.

## Running the tests

```bash
python3 -m pytest -v
```

The tests cover the normal cases plus the things that should fail: depositing a
negative amount, withdrawing too much, transferring with not enough money, and
making sure the saved data loads back correctly.
