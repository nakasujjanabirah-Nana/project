import json
import math
from datetime import datetime
from pathlib import Path

from flask import Flask, abort, redirect, render_template, request, url_for

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "flask_app.json"
task_manager = Flask(__name__, template_folder=str(BASE_DIR / "templates"))
EMPTY_DATA = {
    "branches": [],
    "clients": [],
    "accounts": [],
    "transactions": [],
}


def load_data():
    if not DATA_FILE.exists():
        return {key: records.copy() for key, records in EMPTY_DATA.items()}

    with DATA_FILE.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if data == []:
        data = {key: records.copy() for key, records in EMPTY_DATA.items()}

    if not isinstance(data, dict):
        raise ValueError("flask_app.json must contain a JSON object.")

    for key in EMPTY_DATA:
        records = data.setdefault(key, [])
        if not isinstance(records, list):
            raise ValueError(f"The {key} value in flask_app.json must be a list.")
    return data


def save_data(data):
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)

@task_manager.route("/")
def home():
    return render_template("main.html")


@task_manager.route("/branch", methods=["GET", "POST"])
def branch():
    data = load_data()
    if request.method == "POST":
        data["branches"].append({
            "branch_name": request.form["branch_name"].strip(),
            "address": request.form["address"].strip(),
            "bank_manager": request.form["bank_manager"].strip(),
            "contact": request.form["contact"].strip(),
        })
        save_data(data)
        return redirect(url_for("branch"))
    return render_template("branch.html", branches=data["branches"])


@task_manager.route("/client", methods=["GET", "POST"])
def client():
    data = load_data()
    if request.method == "POST":
        data["clients"].append({
            "Id": f"CL-{len(data['clients']) + 1:04d}",
            "first_name": request.form["first_name"].strip(),
            "last_name": request.form["last_name"].strip(),
            "address": request.form["address"].strip(),
            "contact": request.form["contact"].strip(),
            "gender": request.form["gender"],
        })
        save_data(data)
        return redirect(url_for("client"))
    return render_template("client.html", clients=data["clients"])


@task_manager.route("/accounts", methods=["GET", "POST"])
def accounts():
    data = load_data()
    if request.method == "POST":
        selected_client = next(
            (saved_client for saved_client in data["clients"]
             if saved_client.get("Id") == request.form["client_id"]),
            None,
        )
        if selected_client is None:
            abort(400, description="Select an existing client.")
        if not any(
            saved_branch.get("branch_name") == request.form["branch"]
            for saved_branch in data["branches"]
        ):
            abort(400, description="Select an existing branch.")

        data["accounts"].append({
            "account_number": f"ACC-{len(data['accounts']) + 1:04d}",
            "client_id": selected_client["Id"],
            "account_holder": (
                f"{selected_client['first_name']} {selected_client['last_name']}"
            ),
            "account_type": request.form["account_type"],
            "branch": request.form["branch"],
            "balance": 0.0,
            "date": request.form.get("date", ""),
        })
        save_data(data)
        return redirect(url_for("accounts"))
    return render_template(
        "accounts.html",
        clients=data["clients"],
        branches=data["branches"],
        accounts=data["accounts"],
    )


@task_manager.route("/transactions", methods=["GET", "POST"])
def transactions():
    data = load_data()
    if request.method == "POST":
        transaction_type = request.form["transaction_type"]
        if transaction_type not in {"deposit", "withdrawal", "transfer"}:
            abort(400, description="Select a valid transaction type.")

        try:
            amount = float(request.form["amount"])
        except ValueError:
            abort(400, description="Enter a valid transaction amount.")
        if not math.isfinite(amount) or amount <= 0:
            abort(400, description="The transaction amount must be greater than zero.")

        account_number = request.form["account_number"]
        source_account = next(
            (account for account in data["accounts"]
             if account.get("account_number") == account_number),
            None,
        )
        if source_account is None:
            abort(400, description="Select an existing account.")

        receiver_account = request.form.get("receiver_account", "").strip()
        destination_account = None
        if transaction_type == "transfer":
            if not receiver_account or receiver_account == account_number:
                abort(400, description="Select a different receiving account.")
            destination_account = next(
                (account for account in data["accounts"]
                 if account.get("account_number") == receiver_account),
                None,
            )
            if destination_account is None:
                abort(400, description="The receiving account was not found.")

        balance = float(source_account.get("balance", 0))
        if transaction_type != "deposit" and amount > balance:
            abort(400, description="There are insufficient funds for this transaction.")

        if transaction_type == "deposit":
            source_account["balance"] = balance + amount
        else:
            source_account["balance"] = balance - amount
            if destination_account is not None:
                destination_account["balance"] = (
                    float(destination_account.get("balance", 0)) + amount
                )

        source_balance_after = source_account["balance"]

        transaction = {
            "transaction_id": f"TR-{len(data['transactions']) + 1:04d}",
            "receipt_id": f"RC-{len(data['transactions']) + 1:04d}",
            "transaction_type": transaction_type,
            "date": datetime.now().isoformat(timespec="seconds"),
            "account_number": account_number,
            "amount": amount,
            "source_balance_after": source_balance_after,
        }
        if transaction_type == "transfer":
            transaction["receiver_account"] = receiver_account
            transaction["receiver_balance_after"] = destination_account["balance"]
        data["transactions"].append(transaction)
        save_data(data)
        return redirect(url_for("transactions"))

    return render_template(
        "transaction.html",
        accounts=data["accounts"],
        transactions=data["transactions"],
    )


if __name__ == "__main__":
    task_manager.run(debug=True)
