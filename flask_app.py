import json
import math
from datetime import date, datetime
from pathlib import Path

from flask import Flask, json, request, send_from_directory


app = Flask(__name__)
DATA_DIR = Path(__file__).resolve().parent
PAGES = {"main.html", "branch.html", "client.html", "accounts.html", "transaction.html"}


def read_json(filename, default):
    path = DATA_DIR / filename
    if not path.exists():
        return default
    with path.open(encoding="utf-8") as file:
        return json.load(file)


def write_json(filename, data):
    with (DATA_DIR / filename).open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


def get_records(filename, key):
    data = read_json(filename, [])
    if isinstance(data, list):
        records = data
    elif isinstance(data, dict) and isinstance(data.get(key, []), list):
        records = data.get(key, [])
    else:
        raise ValueError(f"{filename} must contain a list of {key}.")
    return [record for record in records if record != {}]


def get_branches():
    return get_records("branch.json", "branches")


def get_accounts():
    accounts = get_records("accounts.json", "accounts")
    if accounts:
        return accounts
    branch_data = read_json("branch.json", {})
    if isinstance(branch_data, dict) and isinstance(branch_data.get("accounts"), list):
        return [account for account in branch_data["accounts"] if account != {}]
    return accounts


def save_branches(branches):
    data = read_json("branch.json", {})
    if isinstance(data, list):
        data = {"branches": data}
    elif not isinstance(data, dict):
        data = {}
    data["branches"] = branches
    write_json("branch.json", data)


def save_accounts(accounts):
    write_json("accounts.json", accounts)
    data = read_json("branch.json", {})
    if isinstance(data, list):
        data = {"branches": data}
    elif not isinstance(data, dict):
        data = {}
    data["accounts"] = accounts
    write_json("branch.json", data)


def new_id(records, field, prefix):
    existing = {str(record.get(field, "")) for record in records}
    number = 1
    while f"{prefix}-{number:04d}" in existing:
        number += 1
    return f"{prefix}-{number:04d}"


def error(message, status=400):
    return json.dumps({"error": message}), status


def required_text(data, field):
    value = data.get(field)
    return value.strip() if isinstance(value, str) else ""


@app.get("/")
def home():
    return send_from_directory(DATA_DIR, "main.html")


@app.get("/<path:page>")
def show_page(page):
    if page in PAGES:
        return send_from_directory(DATA_DIR, page)
    return error("Page not found.", 404)


@app.get("/api/branches")
def list_branches():
    return json.dumps(get_branches())


@app.post("/api/branches")
def add_branch():
    data = request.get_json(silent=True) or {}
    fields = ("branch_name", "address", "bank_manager", "contact")
    values = {field: required_text(data, field) for field in fields}
    if not all(values.values()):
        return error("Branch name, address, bank manager, and contact are required.")

    branches = get_branches()
    branch = {"branch_code": new_id(branches, "branch_code", "BR"), **values}
    branches.append(branch)
    save_branches(branches)
    return json.dumps(branch), 201


@app.get("/api/clients")
def list_clients():
    return json.dumps(get_records("client.json", "clients"))


@app.post("/api/clients")
def add_client():
    data = request.get_json(silent=True) or {}
    fields = ("first_name", "last_name", "address", "contact", "gender")
    values = {field: required_text(data, field) for field in fields}
    if not all(values.values()):
        return error("First name, last name, address, contact, and gender are required.")

    clients = get_records("client.json", "clients")
    client = {"Id": new_id(clients, "Id", "CL"), **values}
    clients.append(client)
    write_json("client.json", {"clients": clients})
    return json.dumps(client), 201


@app.get("/api/accounts")
def list_accounts():
    return json.dumps(get_accounts())


@app.post("/api/accounts")
def add_account():
    data = request.get_json(silent=True) or {}
    client_id = required_text(data, "client_id")
    account_type = required_text(data, "account_type")
    branch_name = required_text(data, "branch")
    if not client_id or not account_type or not branch_name:
        return error("Client, account type, and branch are required.")

    clients = get_records("client.json", "clients")
    client = next((item for item in clients if item.get("Id") == client_id), None)
    if client is None:
        return error("Client not found.", 404)
    if not any(item.get("branch_name") == branch_name for item in get_branches()):
        return error("Branch not found.", 404)

    accounts = get_accounts()
    account = {
        "account_number": new_id(accounts, "account_number", "ACC"),
        "client_id": client_id,
        "account_type": account_type,
        "account_holder": f"{client.get('first_name', '')} {client.get('last_name', '')}".strip(),
        "branch": branch_name,
        "balance": 0,
        "status": "in progress",
        "date": required_text(data, "date") or date.today().isoformat(),
    }
    accounts.append(account)
    save_accounts(accounts)
    return json.dumps(account), 201


@app.get("/api/transactions")
def list_transactions():
    return json.dumps(get_records("transactions.json", "transactions"))


@app.post("/api/transactions")
def add_transaction():
    data = request.get_json(silent=True) or {}
    transaction_type = required_text(data, "transaction_type").lower()
    account_number = required_text(data, "account_number")
    if transaction_type not in {"deposit", "withdrawal", "transfer"}:
        return error("Transaction type must be deposit, withdrawal, or transfer.")
    try:
        amount = float(data.get("amount"))
    except (TypeError, ValueError):
        return error("Amount must be a valid number.")
    if not math.isfinite(amount) or amount <= 0:
        return error("Amount must be greater than zero.")

    accounts = get_accounts()
    account = next((item for item in accounts if item.get("account_number") == account_number), None)
    if account is None:
        return error("Account not found.", 404)

    receiver_number = required_text(data, "receiver_account")
    receiver = None
    if transaction_type == "transfer":
        if not receiver_number or receiver_number == account_number:
            return error("Choose a different receiving account.")
        receiver = next(
            (item for item in accounts if item.get("account_number") == receiver_number),
            None,
        )
        if receiver is None:
            return error("Receiving account not found.", 404)

    balance = float(account.get("balance", 0))
    if transaction_type in {"withdrawal", "transfer"} and amount > balance:
        return error("Not enough money in the account.")

    if transaction_type == "deposit":
        account["balance"] = round(balance + amount, 2)
    else:
        account["balance"] = round(balance - amount, 2)
        if receiver is not None:
            receiver["balance"] = round(float(receiver.get("balance", 0)) + amount, 2)
    save_accounts(accounts)

    transactions = get_records("transactions.json", "transactions")
    transaction = {
        "transaction_id": new_id(transactions, "transaction_id", "TR"),
        "receipt_id": new_id(transactions, "receipt_id", "RC"),
        "transaction_type": transaction_type,
        "date": datetime.now().isoformat(timespec="seconds"),
        "account_number": account_number,
        "amount": round(amount, 2),
    }
    if receiver is not None:
        transaction["receiver_account"] = receiver_number
    transactions.append(transaction)
    write_json("transactions.json", transactions)
    return json.dumps(transaction), 201


if __name__ == "__main__":
    app.run(debug=True)
