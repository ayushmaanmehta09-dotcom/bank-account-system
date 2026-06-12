from flask import Flask, render_template, request, redirect, url_for, flash

from src.services.bank_service import BankService


def create_app(storage=None):
    app = Flask(__name__)
    app.secret_key = "programming-lab-bank"   # used by Flask to sign flash messages
    service = BankService(storage) if storage else BankService()

    @app.route("/")
    def index():
        return render_template(
            "index.html",
            customers=service.customers,
            accounts=service.all_accounts(),
        )

    @app.route("/customers", methods=["POST"])
    def add_customer():
        name = request.form.get("name", "").strip()
        try:
            service.create_customer(name)
            flash(f"Customer '{name}' created.", "success")
        except ValueError as e:
            flash(str(e), "error")
        return redirect(url_for("index"))

    @app.route("/accounts", methods=["POST"])
    def open_account():
        try:
            customer_id = int(request.form.get("customer_id"))
            opening = float(request.form.get("opening_balance") or 0)
            acc = service.open_account(customer_id, opening)
            flash(f"Opened account #{acc.account_number}.", "success")
        except (ValueError, TypeError) as e:
            flash(str(e), "error")
        return redirect(url_for("index"))

    @app.route("/accounts/<int:number>")
    def account_detail(number):
        account = service.find_account(number)
        if account is None:
            flash("Account not found.", "error")
            return redirect(url_for("index"))
        return render_template(
            "account.html",
            account=account,
            accounts=service.all_accounts(),
        )

    @app.route("/accounts/<int:number>/deposit", methods=["POST"])
    def deposit(number):
        _money_action(service.deposit, number, "Deposited")
        return redirect(url_for("account_detail", number=number))

    @app.route("/accounts/<int:number>/withdraw", methods=["POST"])
    def withdraw(number):
        _money_action(service.withdraw, number, "Withdrew")
        return redirect(url_for("account_detail", number=number))

    @app.route("/accounts/<int:number>/transfer", methods=["POST"])
    def transfer(number):
        try:
            target = int(request.form.get("target"))
            amount = float(request.form.get("amount"))
            service.transfer(number, target, amount)
            flash(f"Transferred {amount:.2f} to #{target}.", "success")
        except (ValueError, TypeError) as e:
            flash(str(e), "error")
        return redirect(url_for("account_detail", number=number))

    def _money_action(func, number, verb):
        # Shared helper so deposit and withdraw don't repeat the same try/except.
        try:
            amount = float(request.form.get("amount"))
            func(number, amount)
            flash(f"{verb} {amount:.2f}.", "success")
        except (ValueError, TypeError) as e:
            flash(str(e), "error")

    return app
